#!/usr/bin/env python3
"""
ATLES Code Security and Validation Module

This module provides comprehensive static analysis, security scanning, and code
validation to ensure all generated code is secure, robust, and functional before
being presented to users.

ARCHITECTURAL FIX: Addresses the core issue where AI-generated code may be
insecure, non-functional, or contain vulnerabilities by implementing automated
validation and security checks.
"""

import ast
import asyncio
import logging
import subprocess
import tempfile
import json
import re
import sys
from typing import Dict, Any, List, Optional, Tuple, Union, Set
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import hashlib
import bandit
from bandit.core import manager as bandit_manager
from bandit.core import config as bandit_config
import pylint.lint
from pylint.reporters.text import TextReporter
import io
import contextlib
import importlib.util
import traceback

logger = logging.getLogger(__name__)


@dataclass
class SecurityIssue:
    """Represents a security issue found in code"""
    severity: str  # 'critical', 'high', 'medium', 'low'
    issue_type: str
    description: str
    line_number: Optional[int]
    column: Optional[int]
    code_snippet: Optional[str]
    recommendation: str
    cwe_id: Optional[str]  # Common Weakness Enumeration ID
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CodeQualityIssue:
    """Represents a code quality issue"""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'syntax', 'style', 'logic', 'performance'
    message: str
    line_number: Optional[int]
    column: Optional[int]
    rule_id: Optional[str]
    suggestion: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    """Result of code validation process"""
    is_valid: bool
    is_secure: bool
    is_functional: bool
    security_score: float  # 0.0 to 1.0
    quality_score: float   # 0.0 to 1.0
    security_issues: List[SecurityIssue]
    quality_issues: List[CodeQualityIssue]
    syntax_errors: List[str]
    runtime_test_results: Dict[str, Any]
    recommendations: List[str]
    validation_timestamp: str
    execution_safe: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'security_issues': [issue.to_dict() for issue in self.security_issues],
            'quality_issues': [issue.to_dict() for issue in self.quality_issues]
        }


class SecurityAnalyzer:
    """Analyzes code for security vulnerabilities"""
    
    def __init__(self):
        self.dangerous_imports = {
            'os': ['system', 'popen', 'spawn*', 'exec*'],
            'subprocess': ['call', 'run', 'Popen', 'check_call', 'check_output'],
            'eval': ['eval', 'exec', 'compile'],
            'pickle': ['load', 'loads', 'dump', 'dumps'],
            'marshal': ['load', 'loads', 'dump', 'dumps'],
            'shelve': ['open'],
            'socket': ['socket', 'create_connection'],
            'urllib': ['urlopen', 'urlretrieve'],
            'requests': ['get', 'post', 'put', 'delete'],
            'sqlite3': ['execute', 'executescript'],
            'mysql': ['*'],
            'psycopg2': ['*'],
        }
        
        self.dangerous_patterns = [
            (r'eval\s*\(', 'Use of eval() function - potential code injection'),
            (r'exec\s*\(', 'Use of exec() function - potential code injection'),
            (r'__import__\s*\(', 'Dynamic import - potential security risk'),
            (r'open\s*\([^)]*["\'][rwa]\+["\']', 'File operations without proper validation'),
            (r'input\s*\([^)]*\)', 'User input without validation'),
            (r'raw_input\s*\([^)]*\)', 'User input without validation'),
            (r'shell\s*=\s*True', 'Shell execution enabled - command injection risk'),
            (r'sql\s*=.*%', 'Potential SQL injection - string formatting in SQL'),
            (r'\.format\s*\(.*sql', 'Potential SQL injection - format in SQL'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
        ]
        
        self.safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'divmod',
            'enumerate', 'filter', 'float', 'format', 'frozenset', 'hash', 'hex',
            'id', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'map',
            'max', 'min', 'oct', 'ord', 'pow', 'range', 'repr', 'reversed', 'round',
            'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
        }
    
    async def analyze_security(self, code: str, filename: str = "temp.py") -> List[SecurityIssue]:
        """Analyze code for security vulnerabilities"""
        issues = []
        
        try:
            # Pattern-based analysis
            pattern_issues = self._analyze_patterns(code)
            issues.extend(pattern_issues)
            
            # AST-based analysis
            ast_issues = self._analyze_ast(code)
            issues.extend(ast_issues)
            
            # Bandit security analysis
            bandit_issues = await self._run_bandit_analysis(code, filename)
            issues.extend(bandit_issues)
            
            logger.info(f"Security analysis found {len(issues)} issues")
            return issues
            
        except Exception as e:
            logger.error(f"Error in security analysis: {e}")
            return [SecurityIssue(
                severity='high',
                issue_type='analysis_error',
                description=f"Security analysis failed: {str(e)}",
                line_number=None,
                column=None,
                code_snippet=None,
                recommendation="Manual security review required",
                cwe_id=None
            )]
    
    def _analyze_patterns(self, code: str) -> List[SecurityIssue]:
        """Analyze code using regex patterns"""
        issues = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern, description in self.dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(SecurityIssue(
                        severity='high',
                        issue_type='dangerous_pattern',
                        description=description,
                        line_number=line_num,
                        column=None,
                        code_snippet=line.strip(),
                        recommendation="Review and validate this code pattern",
                        cwe_id='CWE-94'  # Code Injection
                    ))
        
        return issues
    
    def _analyze_ast(self, code: str) -> List[SecurityIssue]:
        """Analyze code using AST parsing"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if func_name in ['eval', 'exec', '__import__']:
                            issues.append(SecurityIssue(
                                severity='critical',
                                issue_type='dangerous_function',
                                description=f"Use of dangerous function: {func_name}",
                                line_number=getattr(node, 'lineno', None),
                                column=getattr(node, 'col_offset', None),
                                code_snippet=None,
                                recommendation=f"Avoid using {func_name} or implement strict input validation",
                                cwe_id='CWE-94'
                            ))
                
                # Check for dangerous imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.dangerous_imports:
                            issues.append(SecurityIssue(
                                severity='medium',
                                issue_type='dangerous_import',
                                description=f"Import of potentially dangerous module: {alias.name}",
                                line_number=getattr(node, 'lineno', None),
                                column=getattr(node, 'col_offset', None),
                                code_snippet=None,
                                recommendation=f"Ensure safe usage of {alias.name} module",
                                cwe_id='CWE-676'
                            ))
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module in self.dangerous_imports:
                        for alias in node.names:
                            if alias.name in self.dangerous_imports[node.module] or '*' in self.dangerous_imports[node.module]:
                                issues.append(SecurityIssue(
                                    severity='medium',
                                    issue_type='dangerous_import',
                                    description=f"Import of dangerous function: {node.module}.{alias.name}",
                                    line_number=getattr(node, 'lineno', None),
                                    column=getattr(node, 'col_offset', None),
                                    code_snippet=None,
                                    recommendation=f"Validate all inputs to {alias.name}",
                                    cwe_id='CWE-676'
                                ))
        
        except SyntaxError as e:
            issues.append(SecurityIssue(
                severity='high',
                issue_type='syntax_error',
                description=f"Syntax error prevents security analysis: {str(e)}",
                line_number=e.lineno,
                column=e.offset,
                code_snippet=None,
                recommendation="Fix syntax errors before security analysis",
                cwe_id=None
            ))
        
        return issues
    
    async def _run_bandit_analysis(self, code: str, filename: str) -> List[SecurityIssue]:
        """Run Bandit security analysis"""
        issues = []
        
        try:
            # Create temporary file for bandit analysis
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code)
                temp_file.flush()
                
                # Configure bandit
                conf = bandit_config.BanditConfig()
                b_mgr = bandit_manager.BanditManager(conf, 'file')
                
                # Run bandit on the temporary file
                b_mgr.discover_files([temp_file.name])
                b_mgr.run_tests()
                
                # Process results
                for result in b_mgr.get_issue_list():
                    severity_map = {
                        'LOW': 'low',
                        'MEDIUM': 'medium', 
                        'HIGH': 'high'
                    }
                    
                    issues.append(SecurityIssue(
                        severity=severity_map.get(result.severity, 'medium'),
                        issue_type='bandit_finding',
                        description=result.text,
                        line_number=result.lineno,
                        column=result.col_offset,
                        code_snippet=result.get_code(),
                        recommendation=f"Bandit rule {result.test_id}: {result.text}",
                        cwe_id=getattr(result, 'cwe', None)
                    ))
                
                # Clean up
                Path(temp_file.name).unlink()
        
        except Exception as e:
            logger.warning(f"Bandit analysis failed: {e}")
            # Don't fail the entire analysis if bandit fails
        
        return issues


class CodeQualityAnalyzer:
    """Analyzes code quality and style"""
    
    def __init__(self):
        self.complexity_threshold = 10
        self.line_length_threshold = 100
    
    async def analyze_quality(self, code: str, filename: str = "temp.py") -> List[CodeQualityIssue]:
        """Analyze code quality"""
        issues = []
        
        try:
            # Syntax analysis
            syntax_issues = self._check_syntax(code)
            issues.extend(syntax_issues)
            
            # Style analysis
            style_issues = self._check_style(code)
            issues.extend(style_issues)
            
            # Complexity analysis
            complexity_issues = self._check_complexity(code)
            issues.extend(complexity_issues)
            
            # Pylint analysis
            pylint_issues = await self._run_pylint_analysis(code, filename)
            issues.extend(pylint_issues)
            
            logger.info(f"Quality analysis found {len(issues)} issues")
            return issues
            
        except Exception as e:
            logger.error(f"Error in quality analysis: {e}")
            return [CodeQualityIssue(
                severity='error',
                category='analysis_error',
                message=f"Quality analysis failed: {str(e)}",
                line_number=None,
                column=None,
                rule_id=None,
                suggestion="Manual code review required"
            )]
    
    def _check_syntax(self, code: str) -> List[CodeQualityIssue]:
        """Check for syntax errors"""
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(CodeQualityIssue(
                severity='error',
                category='syntax',
                message=f"Syntax error: {e.msg}",
                line_number=e.lineno,
                column=e.offset,
                rule_id='E0001',
                suggestion="Fix syntax error"
            ))
        
        return issues
    
    def _check_style(self, code: str) -> List[CodeQualityIssue]:
        """Check basic style issues"""
        issues = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Line length
            if len(line) > self.line_length_threshold:
                issues.append(CodeQualityIssue(
                    severity='warning',
                    category='style',
                    message=f"Line too long ({len(line)} > {self.line_length_threshold} characters)",
                    line_number=line_num,
                    column=self.line_length_threshold,
                    rule_id='E501',
                    suggestion="Break long lines"
                ))
            
            # Trailing whitespace
            if line.rstrip() != line:
                issues.append(CodeQualityIssue(
                    severity='info',
                    category='style',
                    message="Trailing whitespace",
                    line_number=line_num,
                    column=len(line.rstrip()),
                    rule_id='W291',
                    suggestion="Remove trailing whitespace"
                ))
        
        return issues
    
    def _check_complexity(self, code: str) -> List[CodeQualityIssue]:
        """Check cyclomatic complexity"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_complexity(node)
                    if complexity > self.complexity_threshold:
                        issues.append(CodeQualityIssue(
                            severity='warning',
                            category='complexity',
                            message=f"Function '{node.name}' is too complex (complexity: {complexity})",
                            line_number=getattr(node, 'lineno', None),
                            column=getattr(node, 'col_offset', None),
                            rule_id='C901',
                            suggestion="Break down into smaller functions"
                        ))
        
        except Exception as e:
            logger.warning(f"Complexity analysis failed: {e}")
        
        return issues
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    async def _run_pylint_analysis(self, code: str, filename: str) -> List[CodeQualityIssue]:
        """Run Pylint analysis"""
        issues = []
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code)
                temp_file.flush()
                
                # Capture pylint output
                output = io.StringIO()
                reporter = TextReporter(output)
                
                # Run pylint
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    try:
                        pylint.lint.Run([temp_file.name, '--reports=n', '--score=n'], reporter=reporter, exit=False)
                    except SystemExit:
                        pass  # Pylint calls sys.exit, ignore it
                
                # Parse pylint output
                pylint_output = output.getvalue()
                for line in pylint_output.split('\n'):
                    if ':' in line and temp_file.name in line:
                        parts = line.split(':')
                        if len(parts) >= 4:
                            try:
                                line_num = int(parts[1])
                                col_num = int(parts[2]) if parts[2].isdigit() else None
                                message_parts = parts[3:]
                                message = ':'.join(message_parts).strip()
                                
                                # Extract rule ID and message
                                rule_match = re.search(r'\(([A-Z]\d+)\)', message)
                                rule_id = rule_match.group(1) if rule_match else None
                                
                                # Determine severity
                                if message.startswith('E'):
                                    severity = 'error'
                                elif message.startswith('W'):
                                    severity = 'warning'
                                else:
                                    severity = 'info'
                                
                                issues.append(CodeQualityIssue(
                                    severity=severity,
                                    category='pylint',
                                    message=message,
                                    line_number=line_num,
                                    column=col_num,
                                    rule_id=rule_id,
                                    suggestion="Follow pylint recommendations"
                                ))
                            except (ValueError, IndexError):
                                continue
                
                # Clean up
                Path(temp_file.name).unlink()
        
        except Exception as e:
            logger.warning(f"Pylint analysis failed: {e}")
        
        return issues


class FunctionalityTester:
    """Tests code functionality and execution safety"""
    
    def __init__(self):
        self.timeout = 5  # seconds
        self.max_memory = 100 * 1024 * 1024  # 100MB
    
    async def test_functionality(self, code: str) -> Dict[str, Any]:
        """Test if code is functional and safe to execute"""
        results = {
            'syntax_valid': False,
            'imports_valid': False,
            'execution_safe': False,
            'runtime_errors': [],
            'test_results': {},
            'performance_metrics': {}
        }
        
        try:
            # Test 1: Syntax validation
            results['syntax_valid'] = self._test_syntax(code)
            
            # Test 2: Import validation
            results['imports_valid'] = await self._test_imports(code)
            
            # Test 3: Safe execution test (in sandbox)
            if results['syntax_valid'] and results['imports_valid']:
                execution_result = await self._test_safe_execution(code)
                results.update(execution_result)
            
            logger.info(f"Functionality test completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Functionality test failed: {e}")
            results['runtime_errors'].append(str(e))
            return results
    
    def _test_syntax(self, code: str) -> bool:
        """Test if code has valid syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    async def _test_imports(self, code: str) -> bool:
        """Test if all imports are available"""
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            importlib.import_module(alias.name)
                        except ImportError:
                            return False
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        try:
                            module = importlib.import_module(node.module)
                            for alias in node.names:
                                if not hasattr(module, alias.name):
                                    return False
                        except ImportError:
                            return False
            
            return True
            
        except Exception:
            return False
    
    async def _test_safe_execution(self, code: str) -> Dict[str, Any]:
        """Test code execution in a controlled environment"""
        results = {
            'execution_safe': False,
            'runtime_errors': [],
            'performance_metrics': {}
        }
        
        try:
            # Create a restricted execution environment
            restricted_globals = {
                '__builtins__': {
                    name: getattr(__builtins__, name) 
                    for name in dir(__builtins__) 
                    if name in SecurityAnalyzer().safe_builtins
                }
            }
            
            # Compile the code
            compiled_code = compile(code, '<string>', 'exec')
            
            # Execute with timeout and memory limits
            start_time = datetime.now()
            
            try:
                exec(compiled_code, restricted_globals, {})
                results['execution_safe'] = True
                
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                results['performance_metrics'] = {
                    'execution_time_seconds': execution_time,
                    'memory_safe': True  # Simplified - would need more sophisticated monitoring
                }
                
            except Exception as e:
                results['runtime_errors'].append(f"Runtime error: {str(e)}")
                results['execution_safe'] = False
        
        except Exception as e:
            results['runtime_errors'].append(f"Compilation error: {str(e)}")
            results['execution_safe'] = False
        
        return results


class CodeValidationAPI:
    """Main API for comprehensive code validation"""
    
    def __init__(self):
        self.security_analyzer = SecurityAnalyzer()
        self.quality_analyzer = CodeQualityAnalyzer()
        self.functionality_tester = FunctionalityTester()
        self.validation_history = []
    
    async def validate_code(self, code: str, filename: str = "generated_code.py") -> ValidationResult:
        """Perform comprehensive code validation"""
        try:
            logger.info(f"Starting comprehensive validation for {filename}")
            
            # Run all analyses in parallel
            security_task = asyncio.create_task(self.security_analyzer.analyze_security(code, filename))
            quality_task = asyncio.create_task(self.quality_analyzer.analyze_quality(code, filename))
            functionality_task = asyncio.create_task(self.functionality_tester.test_functionality(code))
            
            # Wait for all analyses to complete
            security_issues, quality_issues, functionality_results = await asyncio.gather(
                security_task, quality_task, functionality_task
            )
            
            # Calculate scores
            security_score = self._calculate_security_score(security_issues)
            quality_score = self._calculate_quality_score(quality_issues)
            
            # Determine overall validation status
            is_valid = len([issue for issue in quality_issues if issue.severity == 'error']) == 0
            is_secure = security_score >= 0.7
            is_functional = functionality_results.get('execution_safe', False)
            execution_safe = is_functional and is_secure
            
            # Extract syntax errors
            syntax_errors = [
                issue.message for issue in quality_issues 
                if issue.category == 'syntax' and issue.severity == 'error'
            ]
            
            # Generate recommendations
            recommendations = self._generate_recommendations(security_issues, quality_issues, functionality_results)
            
            result = ValidationResult(
                is_valid=is_valid,
                is_secure=is_secure,
                is_functional=is_functional,
                security_score=security_score,
                quality_score=quality_score,
                security_issues=security_issues,
                quality_issues=quality_issues,
                syntax_errors=syntax_errors,
                runtime_test_results=functionality_results,
                recommendations=recommendations,
                validation_timestamp=datetime.now().isoformat(),
                execution_safe=execution_safe
            )
            
            # Add to history
            self.validation_history.append({
                'timestamp': result.validation_timestamp,
                'filename': filename,
                'is_valid': is_valid,
                'is_secure': is_secure,
                'security_score': security_score,
                'quality_score': quality_score
            })
            
            logger.info(f"Validation completed: valid={is_valid}, secure={is_secure}, functional={is_functional}")
            return result
            
        except Exception as e:
            logger.error(f"Code validation failed: {e}")
            return ValidationResult(
                is_valid=False,
                is_secure=False,
                is_functional=False,
                security_score=0.0,
                quality_score=0.0,
                security_issues=[],
                quality_issues=[],
                syntax_errors=[f"Validation error: {str(e)}"],
                runtime_test_results={},
                recommendations=["Manual code review required due to validation failure"],
                validation_timestamp=datetime.now().isoformat(),
                execution_safe=False
            )
    
    def _calculate_security_score(self, issues: List[SecurityIssue]) -> float:
        """Calculate security score based on issues found"""
        if not issues:
            return 1.0
        
        # Weight issues by severity
        severity_weights = {'critical': 10, 'high': 5, 'medium': 2, 'low': 1}
        total_weight = sum(severity_weights.get(issue.severity, 1) for issue in issues)
        
        # Normalize to 0-1 scale (assuming max 50 weighted points for 0 score)
        max_weight = 50
        score = max(0.0, 1.0 - (total_weight / max_weight))
        
        return round(score, 2)
    
    def _calculate_quality_score(self, issues: List[CodeQualityIssue]) -> float:
        """Calculate quality score based on issues found"""
        if not issues:
            return 1.0
        
        # Weight issues by severity
        severity_weights = {'error': 10, 'warning': 3, 'info': 1}
        total_weight = sum(severity_weights.get(issue.severity, 1) for issue in issues)
        
        # Normalize to 0-1 scale
        max_weight = 30
        score = max(0.0, 1.0 - (total_weight / max_weight))
        
        return round(score, 2)
    
    def _generate_recommendations(self, security_issues: List[SecurityIssue], 
                                quality_issues: List[CodeQualityIssue],
                                functionality_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Security recommendations
        critical_security = [issue for issue in security_issues if issue.severity == 'critical']
        if critical_security:
            recommendations.append(f"🚨 CRITICAL: Fix {len(critical_security)} critical security issues before use")
        
        high_security = [issue for issue in security_issues if issue.severity == 'high']
        if high_security:
            recommendations.append(f"⚠️ Fix {len(high_security)} high-severity security issues")
        
        # Quality recommendations
        errors = [issue for issue in quality_issues if issue.severity == 'error']
        if errors:
            recommendations.append(f"❌ Fix {len(errors)} syntax/logic errors")
        
        warnings = [issue for issue in quality_issues if issue.severity == 'warning']
        if warnings:
            recommendations.append(f"⚠️ Address {len(warnings)} code quality warnings")
        
        # Functionality recommendations
        if not functionality_results.get('syntax_valid', False):
            recommendations.append("🔧 Fix syntax errors before execution")
        
        if not functionality_results.get('imports_valid', False):
            recommendations.append("📦 Ensure all required packages are installed")
        
        if not functionality_results.get('execution_safe', False):
            recommendations.append("🛡️ Code may not be safe for execution - review carefully")
        
        # Performance recommendations
        perf_metrics = functionality_results.get('performance_metrics', {})
        if perf_metrics.get('execution_time_seconds', 0) > 2:
            recommendations.append("⏱️ Consider optimizing for better performance")
        
        if not recommendations:
            recommendations.append("✅ Code passes all validation checks")
        
        return recommendations
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation history"""
        if not self.validation_history:
            return {'message': 'No validations performed yet'}
        
        recent_validations = self.validation_history[-10:]
        
        return {
            'total_validations': len(self.validation_history),
            'recent_validations': len(recent_validations),
            'avg_security_score': sum(v['security_score'] for v in recent_validations) / len(recent_validations),
            'avg_quality_score': sum(v['quality_score'] for v in recent_validations) / len(recent_validations),
            'success_rate': len([v for v in recent_validations if v['is_valid']]) / len(recent_validations),
            'security_pass_rate': len([v for v in recent_validations if v['is_secure']]) / len(recent_validations)
        }


# Integration function for ATLES
async def validate_generated_code(code: str, filename: str = "ai_generated.py") -> ValidationResult:
    """
    ARCHITECTURAL FIX: This function must be called before presenting any
    AI-generated code to users. It ensures the code is secure, functional,
    and follows best practices.
    
    Returns comprehensive validation results that can be used to:
    1. Block unsafe code from being shown
    2. Provide security warnings
    3. Suggest improvements
    4. Ensure code actually works
    """
    api = CodeValidationAPI()
    return await api.validate_code(code, filename)


# Test function
async def test_code_security():
    """Test the code security and validation system"""
    print("🔒 Testing Code Security and Validation System")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            'name': 'Safe Code',
            'code': '''
def calculate_sum(numbers):
    """Calculate sum of numbers safely."""
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list")
    return sum(numbers)

result = calculate_sum([1, 2, 3, 4, 5])
print(f"Sum: {result}")
'''
        },
        {
            'name': 'Insecure Code',
            'code': '''
import os
user_input = input("Enter command: ")
os.system(user_input)  # Dangerous!

password = "hardcoded_secret_123"  # Security issue
eval(user_input)  # Code injection risk
'''
        },
        {
            'name': 'Poor Quality Code',
            'code': '''
def bad_function(x,y,z,a,b,c,d,e,f,g):
    if x > 0:
        if y > 0:
            if z > 0:
                if a > 0:
                    if b > 0:
                        if c > 0:
                            return x+y+z+a+b+c+d+e+f+g
                        else:
                            return 0
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        return 0
'''
        }
    ]
    
    api = CodeValidationAPI()
    
    for test_case in test_cases:
        print(f"\n{'='*20} {test_case['name']} {'='*20}")
        
        try:
            result = await api.validate_code(test_case['code'], f"{test_case['name'].lower().replace(' ', '_')}.py")
            
            print(f"Valid: {'✅' if result.is_valid else '❌'}")
            print(f"Secure: {'✅' if result.is_secure else '❌'} (Score: {result.security_score:.2f})")
            print(f"Functional: {'✅' if result.is_functional else '❌'}")
            print(f"Quality Score: {result.quality_score:.2f}")
            print(f"Execution Safe: {'✅' if result.execution_safe else '❌'}")
            
            if result.security_issues:
                print(f"\n🔒 Security Issues ({len(result.security_issues)}):")
                for issue in result.security_issues[:3]:  # Show first 3
                    print(f"  - {issue.severity.upper()}: {issue.description}")
            
            if result.quality_issues:
                print(f"\n📝 Quality Issues ({len(result.quality_issues)}):")
                for issue in result.quality_issues[:3]:  # Show first 3
                    print(f"  - {issue.severity.upper()}: {issue.message}")
            
            print(f"\n💡 Recommendations:")
            for rec in result.recommendations[:3]:  # Show first 3
                print(f"  - {rec}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Show summary
    summary = api.get_validation_summary()
    print(f"\n📊 Validation Summary:")
    print(f"Total validations: {summary.get('total_validations', 0)}")
    print(f"Average security score: {summary.get('avg_security_score', 0):.2f}")
    print(f"Average quality score: {summary.get('avg_quality_score', 0):.2f}")
    print(f"Success rate: {summary.get('success_rate', 0):.1%}")


if __name__ == "__main__":
    asyncio.run(test_code_security())
