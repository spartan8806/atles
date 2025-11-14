#!/usr/bin/env python3
"""
ATLES Document Generation System

This system enables the autonomous system to:
1. Generate papers, reports, and documents for the system to read
2. Handle requests from the chat system
3. Send completed work back to the chat system
4. Enable cross-system information sharing

Features:
- Intelligent document generation
- Request queue management
- Inter-system communication
- Document formatting and storage
- Real-time collaboration between systems
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Types of documents that can be generated"""
    RESEARCH_PAPER = "research_paper"
    TECHNICAL_REPORT = "technical_report"
    ANALYSIS_DOCUMENT = "analysis_document"
    SUMMARY_REPORT = "summary_report"
    INSTRUCTION_MANUAL = "instruction_manual"
    KNOWLEDGE_BASE_ENTRY = "knowledge_base_entry"
    SYSTEM_DOCUMENTATION = "system_documentation"
    USER_GUIDE = "user_guide"


class RequestStatus(Enum):
    """Status of document generation requests"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Request priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class DocumentRequest:
    """Document generation request"""
    request_id: str
    requester_system: str  # "chat_system", "autonomous_system", "user"
    document_type: DocumentType
    title: str
    description: str
    requirements: Dict[str, Any]
    priority: Priority
    deadline: Optional[str] = None
    status: RequestStatus = RequestStatus.PENDING
    created_at: str = None
    updated_at: str = None
    assigned_agent: Optional[str] = None
    progress: float = 0.0
    result_path: Optional[str] = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at


@dataclass
class GeneratedDocument:
    """Generated document metadata"""
    document_id: str
    request_id: str
    title: str
    document_type: DocumentType
    file_path: str
    content_preview: str
    word_count: int
    created_at: str
    created_by: str
    tags: List[str]
    summary: str
    quality_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class InterSystemCommunicator:
    """Handles communication between autonomous and chat systems"""
    
    def __init__(self, system_id: str):
        self.system_id = system_id
        self.message_queue_dir = Path("atles_system_communication")
        self.message_queue_dir.mkdir(exist_ok=True)
        
        # Create system-specific directories
        self.inbox_dir = self.message_queue_dir / f"{system_id}_inbox"
        self.outbox_dir = self.message_queue_dir / f"{system_id}_outbox"
        self.inbox_dir.mkdir(exist_ok=True)
        self.outbox_dir.mkdir(exist_ok=True)
        
        logger.info(f"Inter-system communicator initialized for {system_id}")
    
    async def send_message(self, target_system: str, message_type: str, content: Dict[str, Any]) -> str:
        """Send message to another system"""
        
        message_id = str(uuid.uuid4())
        message = {
            "message_id": message_id,
            "from_system": self.system_id,
            "to_system": target_system,
            "message_type": message_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }
        
        # Save to target system's inbox
        target_inbox = self.message_queue_dir / f"{target_system}_inbox"
        target_inbox.mkdir(exist_ok=True)
        
        message_file = target_inbox / f"{message_id}.json"
        with open(message_file, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2)
        
        logger.info(f"Sent message {message_id} to {target_system}: {message_type}")
        return message_id
    
    async def receive_messages(self) -> List[Dict[str, Any]]:
        """Receive messages from other systems"""
        
        messages = []
        
        for message_file in self.inbox_dir.glob("*.json"):
            try:
                with open(message_file, 'r', encoding='utf-8') as f:
                    message = json.load(f)
                
                messages.append(message)
                
                # Move processed message to archive
                archive_dir = self.inbox_dir / "processed"
                archive_dir.mkdir(exist_ok=True)
                message_file.rename(archive_dir / message_file.name)
                
            except Exception as e:
                logger.error(f"Error processing message {message_file}: {e}")
        
        return messages
    
    async def send_document_request(self, target_system: str, request: DocumentRequest) -> str:
        """Send document generation request to another system"""
        
        return await self.send_message(
            target_system=target_system,
            message_type="document_request",
            content=asdict(request)
        )
    
    async def send_document_completion(self, target_system: str, document: GeneratedDocument) -> str:
        """Send document completion notification"""
        
        return await self.send_message(
            target_system=target_system,
            message_type="document_completed",
            content=document.to_dict()
        )
    
    async def send_status_update(self, target_system: str, request_id: str, status: RequestStatus, progress: float = None) -> str:
        """Send status update for a request"""
        
        content = {
            "request_id": request_id,
            "status": status.value,
            "updated_at": datetime.now().isoformat()
        }
        
        if progress is not None:
            content["progress"] = progress
        
        return await self.send_message(
            target_system=target_system,
            message_type="status_update",
            content=content
        )


class DocumentGenerator:
    """Intelligent document generation system"""
    
    def __init__(self, ollama_client=None):
        self.ollama_client = ollama_client
        self.document_templates = self._load_document_templates()
        self.generation_history = []
        
    def _load_document_templates(self) -> Dict[DocumentType, str]:
        """Load document templates for different types"""
        
        templates = {
            DocumentType.RESEARCH_PAPER: """
# {title}

## Abstract
{abstract}

## Introduction
{introduction}

## Methodology
{methodology}

## Results
{results}

## Discussion
{discussion}

## Conclusion
{conclusion}

## References
{references}
""",
            
            DocumentType.TECHNICAL_REPORT: """
# {title}

## Executive Summary
{executive_summary}

## Technical Overview
{technical_overview}

## Implementation Details
{implementation_details}

## Performance Analysis
{performance_analysis}

## Recommendations
{recommendations}

## Appendices
{appendices}
""",
            
            DocumentType.ANALYSIS_DOCUMENT: """
# {title}

## Analysis Overview
{overview}

## Data Analysis
{data_analysis}

## Key Findings
{key_findings}

## Insights and Patterns
{insights}

## Recommendations
{recommendations}

## Next Steps
{next_steps}
""",
            
            DocumentType.KNOWLEDGE_BASE_ENTRY: """
# {title}

## Overview
{overview}

## Key Concepts
{key_concepts}

## Detailed Information
{detailed_info}

## Examples
{examples}

## Related Topics
{related_topics}

## References
{references}
"""
        }
        
        return templates
    
    async def generate_document(self, request: DocumentRequest) -> GeneratedDocument:
        """Generate a document based on the request"""
        
        logger.info(f"Generating document: {request.title}")
        
        try:
            # Get template for document type
            template = self.document_templates.get(request.document_type)
            if not template:
                raise ValueError(f"No template found for document type: {request.document_type}")
            
            # Generate content sections
            content_sections = await self._generate_content_sections(request)
            
            # Fill template
            document_content = template.format(**content_sections)
            
            # Create document file
            document_id = str(uuid.uuid4())
            documents_dir = Path("atles_generated_documents")
            documents_dir.mkdir(exist_ok=True)
            
            # Create filename
            safe_title = "".join(c for c in request.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}_{document_id[:8]}.md"
            file_path = documents_dir / filename
            
            # Save document
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(document_content)
            
            # Create document metadata
            document = GeneratedDocument(
                document_id=document_id,
                request_id=request.request_id,
                title=request.title,
                document_type=request.document_type,
                file_path=str(file_path),
                content_preview=document_content[:500] + "..." if len(document_content) > 500 else document_content,
                word_count=len(document_content.split()),
                created_at=datetime.now().isoformat(),
                created_by="autonomous_document_generator",
                tags=self._extract_tags(request),
                summary=await self._generate_summary(document_content),
                quality_score=await self._assess_quality(document_content)
            )
            
            # Record generation
            self.generation_history.append({
                "request_id": request.request_id,
                "document_id": document_id,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            logger.info(f"Successfully generated document: {filename}")
            return document
            
        except Exception as e:
            logger.error(f"Failed to generate document for request {request.request_id}: {e}")
            
            # Record failure
            self.generation_history.append({
                "request_id": request.request_id,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            })
            
            raise
    
    async def _generate_content_sections(self, request: DocumentRequest) -> Dict[str, str]:
        """Generate content for different sections of the document"""
        
        sections = {}
        
        # Base sections that most documents need
        base_prompt = f"""
Generate content for a {request.document_type.value} titled "{request.title}".

Description: {request.description}

Requirements: {json.dumps(request.requirements, indent=2)}

Please provide detailed, professional content that is:
- Accurate and well-researched
- Clearly structured and organized
- Appropriate for the document type
- Comprehensive yet concise
"""
        
        if request.document_type == DocumentType.RESEARCH_PAPER:
            sections.update({
                "title": request.title,
                "abstract": await self._generate_section(base_prompt + "\n\nGenerate an abstract (150-250 words):"),
                "introduction": await self._generate_section(base_prompt + "\n\nGenerate an introduction section:"),
                "methodology": await self._generate_section(base_prompt + "\n\nGenerate a methodology section:"),
                "results": await self._generate_section(base_prompt + "\n\nGenerate a results section:"),
                "discussion": await self._generate_section(base_prompt + "\n\nGenerate a discussion section:"),
                "conclusion": await self._generate_section(base_prompt + "\n\nGenerate a conclusion:"),
                "references": await self._generate_section(base_prompt + "\n\nGenerate a references section:")
            })
        
        elif request.document_type == DocumentType.TECHNICAL_REPORT:
            sections.update({
                "title": request.title,
                "executive_summary": await self._generate_section(base_prompt + "\n\nGenerate an executive summary:"),
                "technical_overview": await self._generate_section(base_prompt + "\n\nGenerate a technical overview:"),
                "implementation_details": await self._generate_section(base_prompt + "\n\nGenerate implementation details:"),
                "performance_analysis": await self._generate_section(base_prompt + "\n\nGenerate performance analysis:"),
                "recommendations": await self._generate_section(base_prompt + "\n\nGenerate recommendations:"),
                "appendices": await self._generate_section(base_prompt + "\n\nGenerate appendices:")
            })
        
        elif request.document_type == DocumentType.KNOWLEDGE_BASE_ENTRY:
            sections.update({
                "title": request.title,
                "overview": await self._generate_section(base_prompt + "\n\nGenerate an overview section:"),
                "key_concepts": await self._generate_section(base_prompt + "\n\nGenerate key concepts section:"),
                "detailed_info": await self._generate_section(base_prompt + "\n\nGenerate detailed information:"),
                "examples": await self._generate_section(base_prompt + "\n\nGenerate practical examples:"),
                "related_topics": await self._generate_section(base_prompt + "\n\nGenerate related topics:"),
                "references": await self._generate_section(base_prompt + "\n\nGenerate references:")
            })
        
        else:
            # Generic sections for other document types
            sections.update({
                "title": request.title,
                "overview": await self._generate_section(base_prompt + "\n\nGenerate an overview:"),
                "main_content": await self._generate_section(base_prompt + "\n\nGenerate the main content:"),
                "conclusion": await self._generate_section(base_prompt + "\n\nGenerate a conclusion:")
            })
        
        return sections
    
    async def _generate_section(self, prompt: str) -> str:
        """Generate content for a specific section"""
        
        try:
            if self.ollama_client:
                # Use actual AI generation
                response = self.ollama_client.generate("atles-qwen2.5:7b-enhanced", prompt)
                return response if response else "[Content generation failed]"
            else:
                # Fallback to template content
                return f"[Generated content for: {prompt[:100]}...]"
        
        except Exception as e:
            logger.error(f"Error generating section: {e}")
            return f"[Error generating content: {e}]"
    
    async def _generate_summary(self, content: str) -> str:
        """Generate a summary of the document"""
        
        try:
            if self.ollama_client and len(content) > 100:
                summary_prompt = f"Generate a concise summary (2-3 sentences) of this document:\n\n{content[:1000]}..."
                return self.ollama_client.generate("atles-qwen2.5:7b-enhanced", summary_prompt)
            else:
                return "Document summary not available"
        
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Summary generation failed"
    
    async def _assess_quality(self, content: str) -> float:
        """Assess the quality of generated content"""
        
        # Simple quality metrics
        word_count = len(content.split())
        sentence_count = content.count('.') + content.count('!') + content.count('?')
        
        # Basic quality score based on length and structure
        if word_count < 100:
            return 0.3
        elif word_count < 500:
            return 0.6
        elif word_count < 1000:
            return 0.8
        else:
            return 0.9
    
    def _extract_tags(self, request: DocumentRequest) -> List[str]:
        """Extract tags from the request"""
        
        tags = [request.document_type.value]
        
        # Add tags from title and description
        text = f"{request.title} {request.description}".lower()
        
        # Common technical tags
        tech_tags = ["ai", "machine learning", "neural", "algorithm", "system", "analysis", "research", "technical"]
        for tag in tech_tags:
            if tag in text:
                tags.append(tag)
        
        return list(set(tags))


class DocumentGenerationSystem:
    """Main document generation and communication system"""
    
    def __init__(self, system_id: str = "autonomous_system", ollama_client=None):
        self.system_id = system_id
        self.ollama_client = ollama_client
        
        # Initialize components
        self.communicator = InterSystemCommunicator(system_id)
        self.generator = DocumentGenerator(ollama_client)
        
        # Request management
        self.active_requests: Dict[str, DocumentRequest] = {}
        self.completed_documents: Dict[str, GeneratedDocument] = {}
        self.request_queue: List[DocumentRequest] = []
        
        # System state
        self.is_running = False
        self.processing_task = None
        
        logger.info(f"Document generation system initialized for {system_id}")
    
    async def start(self):
        """Start the document generation system"""
        
        self.is_running = True
        self.processing_task = asyncio.create_task(self._process_requests_loop())
        logger.info("Document generation system started")
    
    async def stop(self):
        """Stop the document generation system"""
        
        self.is_running = False
        if self.processing_task:
            self.processing_task.cancel()
        logger.info("Document generation system stopped")
    
    async def create_document_request(self, 
                                    requester_system: str,
                                    document_type: DocumentType,
                                    title: str,
                                    description: str,
                                    requirements: Dict[str, Any] = None,
                                    priority: Priority = Priority.NORMAL,
                                    deadline: str = None) -> str:
        """Create a new document generation request"""
        
        request_id = str(uuid.uuid4())
        request = DocumentRequest(
            request_id=request_id,
            requester_system=requester_system,
            document_type=document_type,
            title=title,
            description=description,
            requirements=requirements or {},
            priority=priority,
            deadline=deadline
        )
        
        # Add to queue and active requests
        self.request_queue.append(request)
        self.active_requests[request_id] = request
        
        # Sort queue by priority
        self.request_queue.sort(key=lambda r: r.priority.value, reverse=True)
        
        logger.info(f"Created document request {request_id}: {title}")
        
        # Notify requester system
        if requester_system != self.system_id:
            await self.communicator.send_status_update(
                requester_system, request_id, RequestStatus.PENDING
            )
        
        return request_id
    
    async def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a document request"""
        
        if request_id in self.active_requests:
            request = self.active_requests[request_id]
            return {
                "request_id": request_id,
                "status": request.status.value,
                "progress": request.progress,
                "title": request.title,
                "created_at": request.created_at,
                "updated_at": request.updated_at
            }
        
        return None
    
    async def get_completed_document(self, document_id: str) -> Optional[GeneratedDocument]:
        """Get a completed document"""
        
        return self.completed_documents.get(document_id)
    
    async def list_documents(self, document_type: DocumentType = None) -> List[Dict[str, Any]]:
        """List generated documents"""
        
        documents = []
        for doc in self.completed_documents.values():
            if document_type is None or doc.document_type == document_type:
                documents.append(doc.to_dict())
        
        return documents
    
    async def _process_requests_loop(self):
        """Main processing loop for document requests"""
        
        while self.is_running:
            try:
                # Process incoming messages
                await self._process_incoming_messages()
                
                # Process document requests
                await self._process_document_requests()
                
                # Wait before next iteration
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(5)
    
    async def _process_incoming_messages(self):
        """Process incoming messages from other systems"""
        
        messages = await self.communicator.receive_messages()
        
        for message in messages:
            try:
                message_type = message.get("message_type")
                content = message.get("content", {})
                from_system = message.get("from_system")
                
                if message_type == "document_request":
                    # Convert content back to DocumentRequest
                    request = DocumentRequest(**content)
                    self.request_queue.append(request)
                    self.active_requests[request.request_id] = request
                    
                    # Sort queue by priority
                    self.request_queue.sort(key=lambda r: r.priority.value, reverse=True)
                    
                    logger.info(f"Received document request from {from_system}: {request.title}")
                
                elif message_type == "status_request":
                    # Send status update
                    request_id = content.get("request_id")
                    if request_id in self.active_requests:
                        request = self.active_requests[request_id]
                        await self.communicator.send_status_update(
                            from_system, request_id, request.status, request.progress
                        )
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def _process_document_requests(self):
        """Process pending document requests"""
        
        if not self.request_queue:
            return
        
        # Get highest priority request
        request = self.request_queue.pop(0)
        
        try:
            # Update status
            request.status = RequestStatus.IN_PROGRESS
            request.updated_at = datetime.now().isoformat()
            
            # Notify requester
            if request.requester_system != self.system_id:
                await self.communicator.send_status_update(
                    request.requester_system, request.request_id, RequestStatus.IN_PROGRESS
                )
            
            logger.info(f"Processing document request: {request.title}")
            
            # Generate document
            document = await self.generator.generate_document(request)
            
            # Update status
            request.status = RequestStatus.COMPLETED
            request.progress = 100.0
            request.result_path = document.file_path
            request.updated_at = datetime.now().isoformat()
            
            # Store completed document
            self.completed_documents[document.document_id] = document
            
            # Notify requester of completion
            if request.requester_system != self.system_id:
                await self.communicator.send_document_completion(
                    request.requester_system, document
                )
            
            logger.info(f"Completed document generation: {document.title}")
            
        except Exception as e:
            # Update status to failed
            request.status = RequestStatus.FAILED
            request.error_message = str(e)
            request.updated_at = datetime.now().isoformat()
            
            # Notify requester of failure
            if request.requester_system != self.system_id:
                await self.communicator.send_status_update(
                    request.requester_system, request.request_id, RequestStatus.FAILED
                )
            
            logger.error(f"Failed to generate document: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        
        return {
            "system_id": self.system_id,
            "is_running": self.is_running,
            "active_requests": len(self.active_requests),
            "queue_length": len(self.request_queue),
            "completed_documents": len(self.completed_documents),
            "total_generated": len(self.generator.generation_history)
        }


# Factory function for easy integration
def create_document_generation_system(system_id: str = "autonomous_system", ollama_client=None) -> DocumentGenerationSystem:
    """Create and return a document generation system"""
    return DocumentGenerationSystem(system_id, ollama_client)
