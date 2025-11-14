#!/usr/bin/env python3
"""
ATLES Source Verification Module

This module provides comprehensive fact-checking and link verification capabilities
to prevent hallucination and ensure all cited sources are authentic and accessible.

ARCHITECTURAL FIX: Forces AI to verify sources before citing them, preventing
the core issue of hallucinated links and unverifiable claims.
"""

import asyncio
import aiohttp
import logging
import json
import re
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, urljoin
import ssl
import certifi
from dataclasses import dataclass, asdict
import time

logger = logging.getLogger(__name__)


@dataclass
class SourceVerificationResult:
    """Result of source verification process"""
    url: str
    is_valid: bool
    status_code: Optional[int]
    response_time_ms: Optional[float]
    content_type: Optional[str]
    title: Optional[str]
    description: Optional[str]
    last_modified: Optional[str]
    verification_timestamp: str
    error_message: Optional[str]
    trust_score: float  # 0.0 to 1.0
    domain_reputation: str  # 'high', 'medium', 'low', 'unknown'
    content_preview: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FactCheckResult:
    """Result of fact-checking process"""
    claim: str
    verification_status: str  # 'verified', 'disputed', 'unverified', 'false'
    confidence_score: float  # 0.0 to 1.0
    supporting_sources: List[SourceVerificationResult]
    contradicting_sources: List[SourceVerificationResult]
    verification_timestamp: str
    fact_check_summary: str
    reliability_assessment: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'supporting_sources': [s.to_dict() for s in self.supporting_sources],
            'contradicting_sources': [s.to_dict() for s in self.contradicting_sources]
        }


class DomainReputationManager:
    """Manages domain reputation and trustworthiness scoring"""
    
    def __init__(self):
        self.trusted_domains = {
            # Academic and Research
            'arxiv.org': {'trust_score': 0.95, 'category': 'academic'},
            'pubmed.ncbi.nlm.nih.gov': {'trust_score': 0.98, 'category': 'academic'},
            'scholar.google.com': {'trust_score': 0.90, 'category': 'academic'},
            'ieee.org': {'trust_score': 0.95, 'category': 'academic'},
            'acm.org': {'trust_score': 0.95, 'category': 'academic'},
            
            # Government and Official
            'gov': {'trust_score': 0.92, 'category': 'government'},  # .gov domains
            'edu': {'trust_score': 0.88, 'category': 'educational'},  # .edu domains
            'who.int': {'trust_score': 0.95, 'category': 'international_org'},
            'un.org': {'trust_score': 0.90, 'category': 'international_org'},
            
            # Technology Documentation
            'docs.python.org': {'trust_score': 0.98, 'category': 'tech_docs'},
            'developer.mozilla.org': {'trust_score': 0.95, 'category': 'tech_docs'},
            'github.com': {'trust_score': 0.85, 'category': 'code_repository'},
            'stackoverflow.com': {'trust_score': 0.80, 'category': 'tech_community'},
            
            # News and Media (Reputable)
            'reuters.com': {'trust_score': 0.85, 'category': 'news'},
            'bbc.com': {'trust_score': 0.85, 'category': 'news'},
            'npr.org': {'trust_score': 0.85, 'category': 'news'},
            'apnews.com': {'trust_score': 0.88, 'category': 'news'},
            
            # Reference and Encyclopedia
            'wikipedia.org': {'trust_score': 0.75, 'category': 'reference'},
            'britannica.com': {'trust_score': 0.85, 'category': 'reference'},
        }
        
        self.suspicious_patterns = [
            r'\.tk$', r'\.ml$', r'\.ga$', r'\.cf$',  # Free domains often used for spam
            r'bit\.ly', r'tinyurl\.com', r't\.co',  # URL shorteners (can hide real destination)
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # Raw IP addresses
        ]
        
        self.reputation_cache = {}
        self.cache_expiry = timedelta(hours=24)
    
    def get_domain_reputation(self, url: str) -> Tuple[float, str]:
        """Get trust score and reputation category for a domain"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check cache first
            cache_key = domain
            if cache_key in self.reputation_cache:
                cached_result, timestamp = self.reputation_cache[cache_key]
                if datetime.now() - timestamp < self.cache_expiry:
                    return cached_result
            
            # Check exact domain match
            if domain in self.trusted_domains:
                info = self.trusted_domains[domain]
                result = (info['trust_score'], info['category'])
                self.reputation_cache[cache_key] = (result, datetime.now())
                return result
            
            # Check TLD-based rules
            for tld_pattern, info in self.trusted_domains.items():
                if domain.endswith(f'.{tld_pattern}'):
                    result = (info['trust_score'], info['category'])
                    self.reputation_cache[cache_key] = (result, datetime.now())
                    return result
            
            # Check for suspicious patterns
            for pattern in self.suspicious_patterns:
                if re.search(pattern, domain):
                    result = (0.2, 'suspicious')
                    self.reputation_cache[cache_key] = (result, datetime.now())
                    return result
            
            # Default for unknown domains
            result = (0.5, 'unknown')
            self.reputation_cache[cache_key] = (result, datetime.now())
            return result
            
        except Exception as e:
            logger.error(f"Error getting domain reputation for {url}: {e}")
            return (0.3, 'error')


class SourceVerifier:
    """Verifies the accessibility and authenticity of web sources"""
    
    def __init__(self):
        self.domain_manager = DomainReputationManager()
        self.verification_cache = {}
        self.cache_expiry = timedelta(hours=6)  # Cache verification results for 6 hours
        
        # SSL context for secure connections
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Common headers to appear as a legitimate browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def verify_source(self, url: str, timeout: int = 10) -> SourceVerificationResult:
        """Verify a single source URL"""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = hashlib.md5(url.encode()).hexdigest()
            if cache_key in self.verification_cache:
                cached_result, timestamp = self.verification_cache[cache_key]
                if datetime.now() - timestamp < self.cache_expiry:
                    logger.info(f"Using cached verification for {url}")
                    return cached_result
            
            # Get domain reputation
            trust_score, domain_reputation = self.domain_manager.get_domain_reputation(url)
            
            # Verify URL accessibility
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            timeout_config = aiohttp.ClientTimeout(total=timeout)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout_config,
                headers=self.headers
            ) as session:
                
                async with session.head(url, allow_redirects=True) as response:
                    response_time_ms = (time.time() - start_time) * 1000
                    
                    # Extract metadata
                    content_type = response.headers.get('content-type', '').split(';')[0]
                    last_modified = response.headers.get('last-modified')
                    
                    # For HTML content, get title and description
                    title = None
                    description = None
                    content_preview = None
                    
                    if content_type.startswith('text/html'):
                        try:
                            async with session.get(url, allow_redirects=True) as full_response:
                                if full_response.status == 200:
                                    html_content = await full_response.text()
                                    title, description, content_preview = self._extract_html_metadata(html_content)
                        except Exception as e:
                            logger.warning(f"Could not extract HTML metadata from {url}: {e}")
                    
                    # Create verification result
                    result = SourceVerificationResult(
                        url=url,
                        is_valid=response.status < 400,
                        status_code=response.status,
                        response_time_ms=response_time_ms,
                        content_type=content_type,
                        title=title,
                        description=description,
                        last_modified=last_modified,
                        verification_timestamp=datetime.now().isoformat(),
                        error_message=None if response.status < 400 else f"HTTP {response.status}",
                        trust_score=trust_score,
                        domain_reputation=domain_reputation,
                        content_preview=content_preview
                    )
                    
                    # Cache the result
                    self.verification_cache[cache_key] = (result, datetime.now())
                    
                    logger.info(f"Verified source {url}: status={response.status}, trust={trust_score:.2f}")
                    return result
        
        except asyncio.TimeoutError:
            result = SourceVerificationResult(
                url=url,
                is_valid=False,
                status_code=None,
                response_time_ms=timeout * 1000,
                content_type=None,
                title=None,
                description=None,
                last_modified=None,
                verification_timestamp=datetime.now().isoformat(),
                error_message="Request timeout",
                trust_score=0.0,
                domain_reputation='timeout',
                content_preview=None
            )
            
        except Exception as e:
            result = SourceVerificationResult(
                url=url,
                is_valid=False,
                status_code=None,
                response_time_ms=(time.time() - start_time) * 1000,
                content_type=None,
                title=None,
                description=None,
                last_modified=None,
                verification_timestamp=datetime.now().isoformat(),
                error_message=str(e),
                trust_score=0.0,
                domain_reputation='error',
                content_preview=None
            )
        
        # Cache failed results too (but with shorter expiry)
        cache_key = hashlib.md5(url.encode()).hexdigest()
        self.verification_cache[cache_key] = (result, datetime.now())
        
        return result
    
    def _extract_html_metadata(self, html_content: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract title, description, and content preview from HTML"""
        try:
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else None
            
            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
            description = desc_match.group(1).strip() if desc_match else None
            
            # Extract content preview (first paragraph or meaningful text)
            # Remove script and style tags
            clean_html = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
            clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.IGNORECASE | re.DOTALL)
            
            # Extract text from paragraphs
            p_matches = re.findall(r'<p[^>]*>(.*?)</p>', clean_html, re.IGNORECASE | re.DOTALL)
            if p_matches:
                # Clean HTML tags and get first meaningful paragraph
                for p in p_matches:
                    clean_p = re.sub(r'<[^>]+>', '', p).strip()
                    if len(clean_p) > 50:  # Meaningful content
                        content_preview = clean_p[:200] + '...' if len(clean_p) > 200 else clean_p
                        break
                else:
                    content_preview = None
            else:
                content_preview = None
            
            return title, description, content_preview
            
        except Exception as e:
            logger.error(f"Error extracting HTML metadata: {e}")
            return None, None, None
    
    async def verify_multiple_sources(self, urls: List[str], max_concurrent: int = 5) -> List[SourceVerificationResult]:
        """Verify multiple sources concurrently"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def verify_with_semaphore(url):
            async with semaphore:
                return await self.verify_source(url)
        
        tasks = [verify_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        verified_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error verifying {urls[i]}: {result}")
                verified_results.append(SourceVerificationResult(
                    url=urls[i],
                    is_valid=False,
                    status_code=None,
                    response_time_ms=None,
                    content_type=None,
                    title=None,
                    description=None,
                    last_modified=None,
                    verification_timestamp=datetime.now().isoformat(),
                    error_message=str(result),
                    trust_score=0.0,
                    domain_reputation='error',
                    content_preview=None
                ))
            else:
                verified_results.append(result)
        
        return verified_results


class FactChecker:
    """Advanced fact-checking system that cross-references claims with verified sources"""
    
    def __init__(self):
        self.source_verifier = SourceVerifier()
        self.fact_check_cache = {}
        self.cache_expiry = timedelta(hours=12)
    
    async def check_claim(self, claim: str, provided_sources: List[str] = None) -> FactCheckResult:
        """Check a factual claim against available sources"""
        try:
            # Check cache first
            cache_key = hashlib.md5(claim.encode()).hexdigest()
            if cache_key in self.fact_check_cache:
                cached_result, timestamp = self.fact_check_cache[cache_key]
                if datetime.now() - timestamp < self.cache_expiry:
                    logger.info(f"Using cached fact-check for claim: {claim[:50]}...")
                    return cached_result
            
            # Verify provided sources
            supporting_sources = []
            contradicting_sources = []
            
            if provided_sources:
                logger.info(f"Verifying {len(provided_sources)} provided sources for claim")
                verification_results = await self.source_verifier.verify_multiple_sources(provided_sources)
                
                # Analyze source content relevance (simplified - in production would use NLP)
                for result in verification_results:
                    if result.is_valid and result.trust_score > 0.5:
                        # Simple keyword matching for relevance (would be more sophisticated in production)
                        if self._is_source_relevant(claim, result):
                            supporting_sources.append(result)
                    else:
                        # Invalid or low-trust sources are considered problematic
                        contradicting_sources.append(result)
            
            # Determine verification status
            verification_status = self._determine_verification_status(supporting_sources, contradicting_sources)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(supporting_sources, contradicting_sources)
            
            # Generate fact-check summary
            fact_check_summary = self._generate_fact_check_summary(
                claim, verification_status, supporting_sources, contradicting_sources
            )
            
            # Assess overall reliability
            reliability_assessment = self._assess_reliability(supporting_sources, contradicting_sources)
            
            result = FactCheckResult(
                claim=claim,
                verification_status=verification_status,
                confidence_score=confidence_score,
                supporting_sources=supporting_sources,
                contradicting_sources=contradicting_sources,
                verification_timestamp=datetime.now().isoformat(),
                fact_check_summary=fact_check_summary,
                reliability_assessment=reliability_assessment
            )
            
            # Cache the result
            self.fact_check_cache[cache_key] = (result, datetime.now())
            
            logger.info(f"Fact-check completed: {verification_status} (confidence: {confidence_score:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error fact-checking claim '{claim}': {e}")
            return FactCheckResult(
                claim=claim,
                verification_status='error',
                confidence_score=0.0,
                supporting_sources=[],
                contradicting_sources=[],
                verification_timestamp=datetime.now().isoformat(),
                fact_check_summary=f"Error during fact-checking: {str(e)}",
                reliability_assessment='unreliable'
            )
    
    def _is_source_relevant(self, claim: str, source_result: SourceVerificationResult) -> bool:
        """Determine if a source is relevant to the claim (simplified implementation)"""
        try:
            claim_lower = claim.lower()
            
            # Check title relevance
            if source_result.title:
                title_lower = source_result.title.lower()
                # Simple keyword overlap check
                claim_words = set(re.findall(r'\b\w+\b', claim_lower))
                title_words = set(re.findall(r'\b\w+\b', title_lower))
                overlap = len(claim_words.intersection(title_words))
                if overlap >= 2:  # At least 2 words in common
                    return True
            
            # Check content preview relevance
            if source_result.content_preview:
                content_lower = source_result.content_preview.lower()
                claim_words = set(re.findall(r'\b\w+\b', claim_lower))
                content_words = set(re.findall(r'\b\w+\b', content_lower))
                overlap = len(claim_words.intersection(content_words))
                if overlap >= 3:  # At least 3 words in common
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking source relevance: {e}")
            return False
    
    def _determine_verification_status(self, supporting_sources: List[SourceVerificationResult], 
                                     contradicting_sources: List[SourceVerificationResult]) -> str:
        """Determine overall verification status"""
        total_support_score = sum(s.trust_score for s in supporting_sources)
        total_contradict_score = sum(s.trust_score for s in contradicting_sources)
        
        if total_support_score >= 2.0 and total_contradict_score < 1.0:
            return 'verified'
        elif total_contradict_score > total_support_score:
            return 'disputed'
        elif total_support_score > 0.5:
            return 'partially_verified'
        else:
            return 'unverified'
    
    def _calculate_confidence_score(self, supporting_sources: List[SourceVerificationResult], 
                                   contradicting_sources: List[SourceVerificationResult]) -> float:
        """Calculate confidence score for the fact-check"""
        if not supporting_sources and not contradicting_sources:
            return 0.0
        
        total_support_score = sum(s.trust_score for s in supporting_sources)
        total_contradict_score = sum(s.trust_score for s in contradicting_sources)
        total_score = total_support_score + total_contradict_score
        
        if total_score == 0:
            return 0.0
        
        # Confidence is based on the proportion of supporting evidence
        confidence = total_support_score / total_score
        
        # Adjust for number of sources (more sources = higher confidence)
        source_count_factor = min(1.0, (len(supporting_sources) + len(contradicting_sources)) / 3.0)
        
        return min(1.0, confidence * source_count_factor)
    
    def _generate_fact_check_summary(self, claim: str, status: str, 
                                   supporting_sources: List[SourceVerificationResult],
                                   contradicting_sources: List[SourceVerificationResult]) -> str:
        """Generate human-readable fact-check summary"""
        summary_parts = [f"Claim: '{claim}'"]
        
        if status == 'verified':
            summary_parts.append(f"✅ VERIFIED: Supported by {len(supporting_sources)} reliable source(s)")
        elif status == 'disputed':
            summary_parts.append(f"❌ DISPUTED: Contradicted by evidence from {len(contradicting_sources)} source(s)")
        elif status == 'partially_verified':
            summary_parts.append(f"⚠️ PARTIALLY VERIFIED: Some supporting evidence found")
        else:
            summary_parts.append(f"❓ UNVERIFIED: Insufficient reliable sources to verify")
        
        # Add source details
        if supporting_sources:
            high_trust_sources = [s for s in supporting_sources if s.trust_score > 0.8]
            if high_trust_sources:
                summary_parts.append(f"High-trust sources include: {', '.join([urlparse(s.url).netloc for s in high_trust_sources[:3]])}")
        
        if contradicting_sources:
            summary_parts.append(f"Issues found with {len(contradicting_sources)} source(s)")
        
        return ". ".join(summary_parts)
    
    def _assess_reliability(self, supporting_sources: List[SourceVerificationResult],
                          contradicting_sources: List[SourceVerificationResult]) -> str:
        """Assess overall reliability of the claim"""
        avg_support_trust = sum(s.trust_score for s in supporting_sources) / max(1, len(supporting_sources))
        
        if avg_support_trust > 0.9 and len(supporting_sources) >= 2:
            return 'highly_reliable'
        elif avg_support_trust > 0.7 and len(supporting_sources) >= 1:
            return 'reliable'
        elif avg_support_trust > 0.5:
            return 'moderately_reliable'
        else:
            return 'unreliable'


class SourceVerificationAPI:
    """Main API for source verification and fact-checking"""
    
    def __init__(self):
        self.source_verifier = SourceVerifier()
        self.fact_checker = FactChecker()
        self.verification_log = []
    
    async def verify_and_check_sources(self, text_with_sources: str) -> Dict[str, Any]:
        """Extract sources from text and verify them comprehensively"""
        try:
            # Extract URLs from text
            urls = self._extract_urls_from_text(text_with_sources)
            
            if not urls:
                return {
                    'status': 'no_sources_found',
                    'message': 'No URLs found in the provided text',
                    'verified_sources': [],
                    'fact_check_results': [],
                    'overall_reliability': 'unverified'
                }
            
            logger.info(f"Found {len(urls)} URLs to verify")
            
            # Verify all sources
            verification_results = await self.source_verifier.verify_multiple_sources(urls)
            
            # Extract claims from text (simplified - would use NLP in production)
            claims = self._extract_claims_from_text(text_with_sources)
            
            # Fact-check claims against verified sources
            fact_check_results = []
            for claim in claims:
                fact_check = await self.fact_checker.check_claim(claim, urls)
                fact_check_results.append(fact_check)
            
            # Calculate overall reliability
            overall_reliability = self._calculate_overall_reliability(verification_results, fact_check_results)
            
            # Log verification
            verification_entry = {
                'timestamp': datetime.now().isoformat(),
                'text_length': len(text_with_sources),
                'urls_found': len(urls),
                'valid_sources': len([r for r in verification_results if r.is_valid]),
                'claims_checked': len(claims),
                'overall_reliability': overall_reliability
            }
            self.verification_log.append(verification_entry)
            
            return {
                'status': 'verification_complete',
                'verified_sources': [r.to_dict() for r in verification_results],
                'fact_check_results': [r.to_dict() for r in fact_check_results],
                'overall_reliability': overall_reliability,
                'summary': self._generate_verification_summary(verification_results, fact_check_results),
                'recommendations': self._generate_recommendations(verification_results, fact_check_results)
            }
            
        except Exception as e:
            logger.error(f"Error in source verification: {e}")
            return {
                'status': 'error',
                'message': f"Verification failed: {str(e)}",
                'verified_sources': [],
                'fact_check_results': [],
                'overall_reliability': 'error'
            }
    
    def _extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text using regex"""
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, text)
        return list(set(urls))  # Remove duplicates
    
    def _extract_claims_from_text(self, text: str) -> List[str]:
        """Extract factual claims from text (simplified implementation)"""
        # This is a simplified implementation - in production would use NLP
        sentences = re.split(r'[.!?]+', text)
        
        claims = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Meaningful length
                # Look for declarative statements
                if not any(word in sentence.lower() for word in ['i think', 'maybe', 'perhaps', 'might']):
                    claims.append(sentence)
        
        return claims[:5]  # Limit to first 5 claims
    
    def _calculate_overall_reliability(self, verification_results: List[SourceVerificationResult],
                                     fact_check_results: List[FactCheckResult]) -> str:
        """Calculate overall reliability score"""
        if not verification_results:
            return 'no_sources'
        
        # Source reliability
        valid_sources = [r for r in verification_results if r.is_valid]
        avg_trust_score = sum(r.trust_score for r in valid_sources) / max(1, len(valid_sources))
        
        # Fact-check reliability
        verified_claims = len([r for r in fact_check_results if r.verification_status == 'verified'])
        total_claims = len(fact_check_results)
        
        if avg_trust_score > 0.8 and (total_claims == 0 or verified_claims / total_claims > 0.7):
            return 'highly_reliable'
        elif avg_trust_score > 0.6 and (total_claims == 0 or verified_claims / total_claims > 0.5):
            return 'reliable'
        elif avg_trust_score > 0.4:
            return 'moderately_reliable'
        else:
            return 'unreliable'
    
    def _generate_verification_summary(self, verification_results: List[SourceVerificationResult],
                                     fact_check_results: List[FactCheckResult]) -> str:
        """Generate human-readable verification summary"""
        valid_sources = len([r for r in verification_results if r.is_valid])
        total_sources = len(verification_results)
        
        summary_parts = [
            f"Verified {valid_sources}/{total_sources} sources"
        ]
        
        if fact_check_results:
            verified_claims = len([r for r in fact_check_results if r.verification_status == 'verified'])
            summary_parts.append(f"{verified_claims}/{len(fact_check_results)} claims verified")
        
        high_trust_sources = [r for r in verification_results if r.trust_score > 0.8]
        if high_trust_sources:
            summary_parts.append(f"{len(high_trust_sources)} high-trust sources")
        
        return ". ".join(summary_parts)
    
    def _generate_recommendations(self, verification_results: List[SourceVerificationResult],
                                fact_check_results: List[FactCheckResult]) -> List[str]:
        """Generate recommendations for improving source reliability"""
        recommendations = []
        
        invalid_sources = [r for r in verification_results if not r.is_valid]
        if invalid_sources:
            recommendations.append(f"Remove {len(invalid_sources)} invalid/inaccessible sources")
        
        low_trust_sources = [r for r in verification_results if r.is_valid and r.trust_score < 0.5]
        if low_trust_sources:
            recommendations.append(f"Consider replacing {len(low_trust_sources)} low-trust sources with more authoritative ones")
        
        disputed_claims = [r for r in fact_check_results if r.verification_status == 'disputed']
        if disputed_claims:
            recommendations.append(f"Review {len(disputed_claims)} disputed claims for accuracy")
        
        if not recommendations:
            recommendations.append("Sources appear reliable - no immediate improvements needed")
        
        return recommendations
    
    async def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics"""
        if not self.verification_log:
            return {'message': 'No verifications performed yet'}
        
        recent_verifications = self.verification_log[-10:]
        
        return {
            'total_verifications': len(self.verification_log),
            'recent_verifications': len(recent_verifications),
            'avg_sources_per_verification': sum(v['urls_found'] for v in recent_verifications) / len(recent_verifications),
            'reliability_distribution': {
                reliability: len([v for v in recent_verifications if v['overall_reliability'] == reliability])
                for reliability in ['highly_reliable', 'reliable', 'moderately_reliable', 'unreliable']
            }
        }


# Integration function for ATLES
async def verify_sources_before_response(response_text: str) -> Dict[str, Any]:
    """
    ARCHITECTURAL FIX: This function must be called before any AI response
    that contains sources or factual claims.
    
    Returns verification results that can be used to modify the response
    or warn about unreliable sources.
    """
    api = SourceVerificationAPI()
    return await api.verify_and_check_sources(response_text)


# Test function
async def test_source_verification():
    """Test the source verification system"""
    print("🔍 Testing Source Verification System")
    print("=" * 50)
    
    # Test text with various sources
    test_text = """
    According to recent research from https://arxiv.org/abs/2301.00001, 
    machine learning models show significant improvement. 
    
    The study from https://invalid-domain-12345.com/fake-study claims otherwise.
    
    Official documentation at https://docs.python.org/3/ provides implementation details.
    """
    
    api = SourceVerificationAPI()
    
    try:
        results = await api.verify_and_check_sources(test_text)
        
        print(f"Status: {results['status']}")
        print(f"Overall Reliability: {results['overall_reliability']}")
        print(f"Summary: {results['summary']}")
        
        print("\nVerified Sources:")
        for source in results['verified_sources']:
            print(f"  - {source['url']}: {'✅' if source['is_valid'] else '❌'} (trust: {source['trust_score']:.2f})")
        
        print("\nRecommendations:")
        for rec in results['recommendations']:
            print(f"  - {rec}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_source_verification())
