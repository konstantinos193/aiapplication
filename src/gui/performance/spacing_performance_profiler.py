"""
Spacing Performance Profiler for comprehensive performance analysis.

This module provides detailed profiling, analysis, and optimization
recommendations for the spacing system.
"""

from typing import Dict, List, Tuple, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import cProfile
import pstats
import io
import threading
from collections import defaultdict, deque
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt6.QtWidgets import QWidget

from ..design_system.spacing_system import SpacingUnit
from ..responsive import responsive_spacing_manager


class ProfilerMode(Enum):
    """Profiling modes for different analysis types."""
    REAL_TIME = "real_time"
    SAMPLING = "sampling"
    TRACE = "trace"
    MEMORY = "memory"
    COMPREHENSIVE = "comprehensive"


class PerformanceMetric(Enum):
    """Types of performance metrics to track."""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    LAYOUT_PASSES = "layout_passes"
    CACHE_HITS = "cache_hits"
    CACHE_MISSES = "cache_misses"
    WIDGET_UPDATES = "widget_updates"


@dataclass
class ProfilerSample:
    """A single performance measurement sample."""
    timestamp: float
    metric_type: PerformanceMetric
    value: float
    context: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[List[str]] = None


@dataclass
class PerformanceReport:
    """Comprehensive performance analysis report."""
    summary: Dict[str, float]
    detailed_metrics: Dict[str, List[ProfilerSample]]
    recommendations: List[str]
    bottlenecks: List[Dict[str, Any]]
    optimization_opportunities: List[Dict[str, Any]]
    generated_at: float = field(default_factory=time.time)


class SpacingPerformanceProfiler(QObject):
    """
    Comprehensive performance profiler for the spacing system.
    
    Features:
    - Real-time performance monitoring
    - Detailed profiling with cProfile integration
    - Memory usage tracking
    - Performance bottleneck identification
    - Optimization recommendations
    - Historical performance analysis
    - Multi-threaded profiling support
    """
    
    # Signals
    performance_alert = pyqtSignal(str, float)  # metric, threshold_exceeded
    bottleneck_detected = pyqtSignal(str, dict)  # bottleneck_type, details
    optimization_recommendation = pyqtSignal(str, str)  # recommendation_type, description
    profile_completed = pyqtSignal(dict)  # profile_results
    
    def __init__(self, 
                 mode: ProfilerMode = ProfilerMode.REAL_TIME,
                 sample_interval: float = 0.1):
        super().__init__()
        self._mode = mode
        self._sample_interval = sample_interval
        self._profiler = cProfile.Profile()
        self._is_profiling = False
        
        # Performance data storage
        self._performance_data: Dict[PerformanceMetric, deque] = defaultdict(
            lambda: deque(maxlen=1000)
        )
        self._function_timings: Dict[str, List[float]] = defaultdict(list)
        self._memory_snapshots: List[Tuple[float, int]] = []
        self._layout_metrics: Dict[str, Dict[str, Any]] = {}
        
        # Thresholds and alerts
        self._performance_thresholds = {
            PerformanceMetric.EXECUTION_TIME: 0.016,  # 16ms (60fps)
            PerformanceMetric.MEMORY_USAGE: 100 * 1024 * 1024,  # 100MB
            PerformanceMetric.CPU_USAGE: 80.0,  # 80%
            PerformanceMetric.LAYOUT_PASSES: 5,  # 5 passes per frame
            PerformanceMetric.CACHE_HITS: 0.7,  # 70% hit rate
            PerformanceMetric.CACHE_MISSES: 0.3,  # 30% miss rate
            PerformanceMetric.WIDGET_UPDATES: 100  # 100 updates per frame
        }
        
        # Profiling threads
        self._profiler_thread: Optional[QThread] = None
        self._profiler_timer = QTimer()
        self._profiler_timer.timeout.connect(self._collect_performance_sample)
        
        # Start profiling if in real-time mode
        if mode == ProfilerMode.REAL_TIME:
            self._start_real_time_profiling()
    
    def start_profiling(self, 
                       mode: Optional[ProfilerMode] = None,
                       duration: Optional[float] = None) -> bool:
        """
        Start performance profiling.
        
        Args:
            mode: Profiling mode (None for current mode)
            duration: Profiling duration in seconds (None for indefinite)
            
        Returns:
            True if profiling started successfully
        """
        if self._is_profiling:
            return False
        
        if mode:
            self._mode = mode
        
        self._is_profiling = True
        
        if self._mode == ProfilerMode.REAL_TIME:
            self._start_real_time_profiling()
        elif self._mode == ProfilerMode.SAMPLING:
            self._start_sampling_profiling()
        elif self._mode == ProfilerMode.TRACE:
            self._start_trace_profiling()
        elif self._mode == ProfilerMode.MEMORY:
            self._start_memory_profiling()
        elif self._mode == ProfilerMode.COMPREHENSIVE:
            self._start_comprehensive_profiling()
        
        # Set duration timer if specified
        if duration:
            QTimer.singleShot(int(duration * 1000), self.stop_profiling)
        
        return True
    
    def stop_profiling(self) -> Optional[PerformanceReport]:
        """
        Stop performance profiling and generate report.
        
        Returns:
            Performance report or None if not profiling
        """
        if not self._is_profiling:
            return None
        
        self._is_profiling = False
        
        # Stop profiling based on mode
        if self._mode == ProfilerMode.REAL_TIME:
            self._stop_real_time_profiling()
        elif self._mode == ProfilerMode.SAMPLING:
            self._stop_sampling_profiling()
        elif self._mode == ProfilerMode.TRACE:
            self._stop_trace_profiling()
        elif self._mode == ProfilerMode.MEMORY:
            self._stop_memory_profiling()
        elif self._mode == ProfilerMode.COMPREHENSIVE:
            self._stop_comprehensive_profiling()
        
        # Generate and return report
        report = self._generate_performance_report()
        self.profile_completed.emit(report.__dict__)
        
        return report
    
    def profile_function(self, 
                        func: Callable,
                        *args,
                        **kwargs) -> Tuple[Any, float]:
        """
        Profile a single function execution.
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Tuple of (function_result, execution_time)
        """
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            execution_time = time.time() - start_time
            self._record_function_timing(func.__name__, execution_time)
            raise e
        
        execution_time = time.time() - start_time
        self._record_function_timing(func.__name__, execution_time)
        
        # Check performance thresholds
        self._check_performance_thresholds(PerformanceMetric.EXECUTION_TIME, execution_time)
        
        return result, execution_time
    
    def profile_spacing_calculation(self, 
                                   base_spacing: Union[int, SpacingUnit],
                                   calculation_type: str,
                                   **kwargs) -> Tuple[int, float]:
        """
        Profile a spacing calculation with detailed metrics.
        
        Args:
            base_spacing: Base spacing value or unit
            calculation_type: Type of calculation
            **kwargs: Additional calculation parameters
            
        Returns:
            Tuple of (calculated_spacing, execution_time)
        """
        start_time = time.time()
        
        # Record memory before calculation
        memory_before = self._get_memory_usage()
        
        try:
            # Perform spacing calculation
            if calculation_type == "responsive":
                result = responsive_spacing_manager.get_responsive_spacing(
                    base_spacing, 
                    kwargs.get('touch_friendly', False)
                )
            else:
                result = get_spacing_value(base_spacing)
            
            execution_time = time.time() - start_time
            memory_after = self._get_memory_usage()
            
            # Record metrics
            self._record_performance_sample(
                PerformanceMetric.EXECUTION_TIME,
                execution_time,
                {'calculation_type': calculation_type, 'base_spacing': str(base_spacing)}
            )
            
            self._record_performance_sample(
                PerformanceMetric.MEMORY_USAGE,
                memory_after - memory_before,
                {'calculation_type': calculation_type}
            )
            
            # Check thresholds
            self._check_performance_thresholds(PerformanceMetric.EXECUTION_TIME, execution_time)
            self._check_performance_thresholds(PerformanceMetric.MEMORY_USAGE, memory_after - memory_before)
            
            return result, execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._record_function_timing(f"spacing_calculation_{calculation_type}", execution_time)
            raise e
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of current performance metrics."""
        summary = {}
        
        for metric, samples in self._performance_data.items():
            if samples:
                values = [sample.value for sample in samples]
                summary[metric.value] = {
                    'current': values[-1] if values else 0,
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'samples': len(values)
                }
        
        # Add function timing summary
        summary['function_timings'] = {}
        for func_name, timings in self._function_timings.items():
            if timings:
                summary['function_timings'][func_name] = {
                    'average': sum(timings) / len(timings),
                    'min': min(timings),
                    'max': max(timings),
                    'calls': len(timings)
                }
        
        # Add memory snapshot summary
        if self._memory_snapshots:
            memory_values = [snapshot[1] for snapshot in self._memory_snapshots]
            summary['memory'] = {
                'current': memory_values[-1] if memory_values else 0,
                'average': sum(memory_values) / len(memory_values),
                'min': min(memory_values),
                'max': max(memory_values),
                'snapshots': len(memory_values)
            }
        
        return summary
    
    def set_performance_threshold(self, 
                                 metric: PerformanceMetric,
                                 threshold: float):
        """Set a performance threshold for alerts."""
        self._performance_thresholds[metric] = threshold
    
    def get_performance_thresholds(self) -> Dict[PerformanceMetric, float]:
        """Get all performance thresholds."""
        return self._performance_thresholds.copy()
    
    def clear_performance_data(self):
        """Clear all collected performance data."""
        self._performance_data.clear()
        self._function_timings.clear()
        self._memory_snapshots.clear()
        self._layout_metrics.clear()
    
    def export_performance_data(self, 
                               format: str = "json") -> str:
        """
        Export performance data in specified format.
        
        Args:
            format: Export format ("json", "csv", "html")
            
        Returns:
            Exported data as string
        """
        if format == "json":
            return self._export_json()
        elif format == "csv":
            return self._export_csv()
        elif format == "html":
            return self._export_html()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _start_real_time_profiling(self):
        """Start real-time performance monitoring."""
        self._profiler_timer.start(int(self._sample_interval * 1000))
    
    def _stop_real_time_profiling(self):
        """Stop real-time performance monitoring."""
        self._profiler_timer.stop()
    
    def _start_sampling_profiling(self):
        """Start sampling-based profiling."""
        self._profiler.enable()
    
    def _stop_sampling_profiling(self):
        """Stop sampling-based profiling."""
        self._profiler.disable()
    
    def _start_trace_profiling(self):
        """Start trace-based profiling."""
        # Enable detailed function tracing
        self._profiler.enable(subcalls=True, builtins=True)
    
    def _stop_trace_profiling(self):
        """Stop trace-based profiling."""
        self._profiler.disable()
    
    def _start_memory_profiling(self):
        """Start memory usage profiling."""
        # Start memory monitoring
        self._memory_snapshots.append((time.time(), self._get_memory_usage()))
    
    def _stop_memory_profiling(self):
        """Stop memory usage profiling."""
        # Final memory snapshot
        self._memory_snapshots.append((time.time(), self._get_memory_usage()))
    
    def _start_comprehensive_profiling(self):
        """Start comprehensive profiling (all modes)."""
        self._start_sampling_profiling()
        self._start_memory_profiling()
        self._start_real_time_profiling()
    
    def _stop_comprehensive_profiling(self):
        """Stop comprehensive profiling."""
        self._stop_sampling_profiling()
        self._stop_memory_profiling()
        self._stop_real_time_profiling()
    
    def _collect_performance_sample(self):
        """Collect a performance sample in real-time mode."""
        if not self._is_profiling:
            return
        
        # Collect current metrics
        current_time = time.time()
        
        # Memory usage
        memory_usage = self._get_memory_usage()
        self._record_performance_sample(PerformanceMetric.MEMORY_USAGE, memory_usage)
        self._memory_snapshots.append((current_time, memory_usage))
        
        # CPU usage (estimated)
        cpu_usage = self._estimate_cpu_usage()
        self._record_performance_sample(PerformanceMetric.CPU_USAGE, cpu_usage)
        
        # Check thresholds
        self._check_performance_thresholds(PerformanceMetric.MEMORY_USAGE, memory_usage)
        self._check_performance_thresholds(PerformanceMetric.CPU_USAGE, cpu_usage)
    
    def _record_performance_sample(self, 
                                  metric: PerformanceMetric,
                                  value: float,
                                  context: Optional[Dict[str, Any]] = None):
        """Record a performance sample."""
        sample = ProfilerSample(
            timestamp=time.time(),
            metric_type=metric,
            value=value,
            context=context or {}
        )
        
        self._performance_data[metric].append(sample)
    
    def _record_function_timing(self, func_name: str, execution_time: float):
        """Record function execution timing."""
        self._function_timings[func_name].append(execution_time)
        
        # Keep only recent timings
        if len(self._function_timings[func_name]) > 100:
            self._function_timings[func_name] = self._function_timings[func_name][-100:]
    
    def _check_performance_thresholds(self, metric: PerformanceMetric, value: float):
        """Check if performance threshold is exceeded."""
        threshold = self._performance_thresholds.get(metric)
        if threshold is not None:
            if metric in [PerformanceMetric.CACHE_HITS, PerformanceMetric.CACHE_MISSES]:
                # For ratios, check if below threshold (lower is worse)
                if value < threshold:
                    self.performance_alert.emit(metric.value, threshold)
            else:
                # For other metrics, check if above threshold (higher is worse)
                if value > threshold:
                    self.performance_alert.emit(metric.value, threshold)
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            # Fallback to basic memory estimation
            return 0
    
    def _estimate_cpu_usage(self) -> float:
        """Estimate current CPU usage percentage."""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            # Fallback to basic estimation
            return 0.0
    
    def _generate_performance_report(self) -> PerformanceReport:
        """Generate a comprehensive performance report."""
        summary = self.get_performance_summary()
        
        # Analyze bottlenecks
        bottlenecks = self._identify_bottlenecks()
        
        # Generate optimization recommendations
        recommendations = self._generate_optimization_recommendations(summary, bottlenecks)
        
        # Identify optimization opportunities
        opportunities = self._identify_optimization_opportunities(summary)
        
        # Convert performance data to report format
        detailed_metrics = {}
        for metric, samples in self._performance_data.items():
            detailed_metrics[metric.value] = list(samples)
        
        return PerformanceReport(
            summary=summary,
            detailed_metrics=detailed_metrics,
            recommendations=recommendations,
            bottlenecks=bottlenecks,
            optimization_opportunities=opportunities
        )
    
    def _identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []
        
        # Check execution time bottlenecks
        if PerformanceMetric.EXECUTION_TIME in self._performance_data:
            samples = self._performance_data[PerformanceMetric.EXECUTION_TIME]
            if samples:
                avg_time = sum(s.value for s in samples) / len(samples)
                if avg_time > 0.016:  # 16ms threshold
                    bottlenecks.append({
                        'type': 'execution_time',
                        'severity': 'high' if avg_time > 0.033 else 'medium',
                        'description': f'Average execution time {avg_time:.3f}s exceeds 16ms threshold',
                        'current_value': avg_time,
                        'threshold': 0.016
                    })
        
        # Check memory bottlenecks
        if PerformanceMetric.MEMORY_USAGE in self._performance_data:
            samples = self._performance_data[PerformanceMetric.MEMORY_USAGE]
            if samples:
                avg_memory = sum(s.value for s in samples) / len(samples)
                if avg_memory > 100 * 1024 * 1024:  # 100MB threshold
                    bottlenecks.append({
                        'type': 'memory_usage',
                        'severity': 'high' if avg_memory > 500 * 1024 * 1024 else 'medium',
                        'description': f'Average memory usage {avg_memory / (1024*1024):.1f}MB exceeds 100MB threshold',
                        'current_value': avg_memory,
                        'threshold': 100 * 1024 * 1024
                    })
        
        # Check function timing bottlenecks
        for func_name, timings in self._function_timings.items():
            if timings:
                avg_time = sum(timings) / len(timings)
                if avg_time > 0.001:  # 1ms threshold for individual functions
                    bottlenecks.append({
                        'type': 'function_timing',
                        'severity': 'high' if avg_time > 0.01 else 'medium',
                        'description': f'Function {func_name} average execution time {avg_time:.3f}s exceeds 1ms threshold',
                        'current_value': avg_time,
                        'threshold': 0.001,
                        'function': func_name
                    })
        
        return bottlenecks
    
    def _generate_optimization_recommendations(self, 
                                             summary: Dict[str, Any],
                                             bottlenecks: List[Dict[str, Any]]) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        recommendations = []
        
        # Execution time recommendations
        if 'execution_time' in summary:
            exec_summary = summary['execution_time']
            if exec_summary['average'] > 0.016:
                recommendations.append("Consider implementing function-level caching for frequently called spacing calculations")
                recommendations.append("Review spacing calculation algorithms for optimization opportunities")
                recommendations.append("Implement batch processing for multiple spacing calculations")
        
        # Memory usage recommendations
        if 'memory_usage' in summary:
            memory_summary = summary['memory_usage']
            if memory_summary['average'] > 100 * 1024 * 1024:
                recommendations.append("Implement memory pooling for spacing calculation objects")
                recommendations.append("Review and optimize spacing cache eviction strategies")
                recommendations.append("Consider implementing lazy loading for spacing resources")
        
        # Cache performance recommendations
        if 'cache_hits' in summary:
            cache_summary = summary['cache_hits']
            if cache_summary['current'] < 0.7:
                recommendations.append("Increase cache size or improve cache key generation")
                recommendations.append("Implement predictive caching for common spacing patterns")
                recommendations.append("Review cache invalidation strategies")
        
        # Function-specific recommendations
        if 'function_timings' in summary:
            func_summary = summary['function_timings']
            slow_functions = [
                (name, data) for name, data in func_summary.items()
                if data['average'] > 0.001
            ]
            
            for func_name, data in slow_functions:
                recommendations.append(f"Profile and optimize function '{func_name}' (avg: {data['average']:.3f}s)")
        
        return recommendations
    
    def _identify_optimization_opportunities(self, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities."""
        opportunities = []
        
        # Look for patterns in performance data
        for metric_name, metric_data in summary.items():
            if isinstance(metric_data, dict) and 'current' in metric_data and 'average' in metric_data:
                current = metric_data['current']
                average = metric_data['average']
                
                # Identify significant deviations from average
                if average > 0:
                    deviation = abs(current - average) / average
                    if deviation > 0.2:  # 20% deviation
                        opportunities.append({
                            'metric': metric_name,
                            'type': 'performance_variance',
                            'description': f'High variance in {metric_name}: current={current:.3f}, average={average:.3f}',
                            'severity': 'high' if deviation > 0.5 else 'medium',
                            'deviation': deviation
                        })
        
        return opportunities
    
    def _export_json(self) -> str:
        """Export performance data as JSON."""
        import json
        return json.dumps(self.get_performance_summary(), indent=2)
    
    def _export_csv(self) -> str:
        """Export performance data as CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        summary = self.get_performance_summary()
        
        # Write headers
        writer.writerow(['Metric', 'Current', 'Average', 'Min', 'Max', 'Samples'])
        
        # Write data
        for metric_name, metric_data in summary.items():
            if isinstance(metric_data, dict) and 'current' in metric_data:
                writer.writerow([
                    metric_name,
                    metric_data.get('current', 0),
                    metric_data.get('average', 0),
                    metric_data.get('min', 0),
                    metric_data.get('max', 0),
                    metric_data.get('samples', 0)
                ])
        
        return output.getvalue()
    
    def _export_html(self) -> str:
        """Export performance data as HTML."""
        summary = self.get_performance_summary()
        
        html = """
        <html>
        <head>
            <title>Performance Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .metric { margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <h1>Performance Report</h1>
            <p>Generated at: {timestamp}</p>
        """.format(timestamp=time.strftime('%Y-%m-%d %H:%M:%S'))
        
        for metric_name, metric_data in summary.items():
            if isinstance(metric_data, dict) and 'current' in metric_data:
                html += f"""
                <div class="metric">
                    <h2>{metric_name}</h2>
                    <table>
                        <tr><th>Property</th><th>Value</th></tr>
                        <tr><td>Current</td><td>{metric_data.get('current', 0):.3f}</td></tr>
                        <tr><td>Average</td><td>{metric_data.get('average', 0):.3f}</td></tr>
                        <tr><td>Min</td><td>{metric_data.get('min', 0):.3f}</td></tr>
                        <tr><td>Max</td><td>{metric_data.get('max', 0):.3f}</td></tr>
                        <tr><td>Samples</td><td>{metric_data.get('samples', 0)}</td></tr>
                    </table>
                </div>
                """
        
        html += """
        </body>
        </html>
        """
        
        return html


# Global instance for easy access
spacing_performance_profiler = SpacingPerformanceProfiler()
