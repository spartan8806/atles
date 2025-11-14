#!/usr/bin/env python3
"""
ATLES Data Visualization Module

This module provides comprehensive data visualization capabilities using both
Matplotlib and Plotly, enabling the AI to generate and display real charts,
graphs, and data visualizations instead of providing non-functional examples.

ARCHITECTURAL FIX: Replaces the AI's inability to provide graphs or direct data
links with actual functional data visualization tools and chart generation.
"""

import asyncio
import logging
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.io as pio
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import base64
import io
from dataclasses import dataclass, asdict
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Configuration for chart generation"""
    chart_type: str
    title: str
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    width: int = 800
    height: int = 600
    theme: str = 'default'  # 'default', 'dark', 'minimal', 'colorful'
    interactive: bool = True
    save_path: Optional[str] = None
    format: str = 'html'  # 'html', 'png', 'svg', 'pdf'
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VisualizationResult:
    """Result of visualization generation"""
    chart_type: str
    title: str
    file_path: Optional[str]
    html_content: Optional[str]
    base64_image: Optional[str]
    interactive_url: Optional[str]
    metadata: Dict[str, Any]
    generation_timestamp: str
    success: bool
    error_message: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DataProcessor:
    """Processes and validates data for visualization"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'json', 'excel', 'parquet']
    
    def load_data(self, data_source: Union[str, Dict, List, pd.DataFrame]) -> pd.DataFrame:
        """Load data from various sources"""
        try:
            if isinstance(data_source, pd.DataFrame):
                return data_source
            
            elif isinstance(data_source, str):
                # File path
                path = Path(data_source)
                if path.exists():
                    if path.suffix.lower() == '.csv':
                        return pd.read_csv(data_source)
                    elif path.suffix.lower() in ['.xlsx', '.xls']:
                        return pd.read_excel(data_source)
                    elif path.suffix.lower() == '.json':
                        return pd.read_json(data_source)
                    elif path.suffix.lower() == '.parquet':
                        return pd.read_parquet(data_source)
                    else:
                        raise ValueError(f"Unsupported file format: {path.suffix}")
                else:
                    # Try to parse as JSON string
                    try:
                        data = json.loads(data_source)
                        return pd.DataFrame(data)
                    except:
                        raise ValueError("Invalid data source: not a valid file path or JSON string")
            
            elif isinstance(data_source, (list, dict)):
                return pd.DataFrame(data_source)
            
            else:
                raise ValueError(f"Unsupported data source type: {type(data_source)}")
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self, df: pd.DataFrame, chart_type: str) -> Tuple[bool, str]:
        """Validate data for specific chart types"""
        try:
            if df.empty:
                return False, "Dataset is empty"
            
            if chart_type in ['line', 'scatter', 'bar']:
                if len(df.columns) < 2:
                    return False, f"{chart_type} chart requires at least 2 columns"
            
            elif chart_type == 'histogram':
                if len(df.columns) < 1:
                    return False, "Histogram requires at least 1 numeric column"
                # Check if we have numeric data
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    return False, "Histogram requires numeric data"
            
            elif chart_type == 'pie':
                if len(df.columns) < 2:
                    return False, "Pie chart requires at least 2 columns (categories and values)"
            
            elif chart_type == 'heatmap':
                # Check if we have numeric data for correlation
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) < 2:
                    return False, "Heatmap requires at least 2 numeric columns"
            
            return True, "Data validation passed"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def prepare_data(self, df: pd.DataFrame, chart_type: str) -> pd.DataFrame:
        """Prepare data for specific chart types"""
        try:
            df_clean = df.copy()
            
            # Handle missing values
            if chart_type in ['line', 'scatter']:
                # For line/scatter plots, we can interpolate numeric data
                numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
                df_clean[numeric_cols] = df_clean[numeric_cols].interpolate()
            else:
                # For other charts, drop rows with missing values
                df_clean = df_clean.dropna()
            
            # Convert date columns (with proper pandas handling)
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    try:
                        # Try to convert to datetime - let pandas handle it automatically
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                        # If conversion resulted in all NaT, revert to original
                        if df_clean[col].isna().all():
                            df_clean[col] = df.copy()[col]
                    except:
                        pass  # Not a date column
            
            return df_clean
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return df


class MatplotlibVisualizer:
    """Creates static visualizations using Matplotlib"""
    
    def __init__(self):
        # Set up matplotlib style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_line_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create line chart"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            # Assume first column is x-axis, rest are y-axis
            x_col = df.columns[0]
            y_cols = df.columns[1:]
            
            for y_col in y_cols:
                ax.plot(df[x_col], df[y_col], label=y_col, marker='o', linewidth=2)
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            ax.set_xlabel(config.x_label or x_col, fontsize=12)
            ax.set_ylabel(config.y_label or 'Values', fontsize=12)
            
            if len(y_cols) > 1:
                ax.legend()
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_bar_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create bar chart"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            bars = ax.bar(df[x_col], df[y_col], color=sns.color_palette("husl", len(df)))
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            ax.set_xlabel(config.x_label or x_col, fontsize=12)
            ax.set_ylabel(config.y_label or y_col, fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_histogram(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create histogram"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            # Use first numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            data_col = numeric_cols[0]
            
            ax.hist(df[data_col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            ax.set_xlabel(config.x_label or data_col, fontsize=12)
            ax.set_ylabel(config.y_label or 'Frequency', fontsize=12)
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_scatter_plot(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create scatter plot"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            # Color by third column if available
            if len(df.columns) > 2:
                c_col = df.columns[2]
                scatter = ax.scatter(df[x_col], df[y_col], c=df[c_col], 
                                   cmap='viridis', alpha=0.7, s=60)
                plt.colorbar(scatter, label=c_col)
            else:
                ax.scatter(df[x_col], df[y_col], alpha=0.7, s=60, color='steelblue')
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            ax.set_xlabel(config.x_label or x_col, fontsize=12)
            ax.set_ylabel(config.y_label or y_col, fontsize=12)
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_pie_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create pie chart"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            labels_col = df.columns[0]
            values_col = df.columns[1]
            
            # Aggregate data if needed
            pie_data = df.groupby(labels_col)[values_col].sum()
            
            colors = sns.color_palette("husl", len(pie_data))
            wedges, texts, autotexts = ax.pie(pie_data.values, labels=pie_data.index, 
                                             autopct='%1.1f%%', colors=colors, startangle=90)
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_heatmap(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create correlation heatmap"""
        try:
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            # Calculate correlation matrix for numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            corr_matrix = numeric_df.corr()
            
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5, ax=ax)
            
            ax.set_title(config.title, fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            return self._save_matplotlib_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def _save_matplotlib_figure(self, fig: plt.Figure, config: ChartConfig) -> VisualizationResult:
        """Save matplotlib figure and return result"""
        try:
            # Save as base64 image
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            base64_image = base64.b64encode(buffer.getvalue()).decode()
            
            # Save to file if path specified
            file_path = None
            if config.save_path:
                file_path = config.save_path
                fig.savefig(file_path, dpi=150, bbox_inches='tight')
            
            plt.close(fig)  # Clean up
            
            return VisualizationResult(
                chart_type=config.chart_type,
                title=config.title,
                file_path=file_path,
                html_content=None,
                base64_image=base64_image,
                interactive_url=None,
                metadata={'renderer': 'matplotlib', 'format': 'png'},
                generation_timestamp=datetime.now().isoformat(),
                success=True,
                error_message=None
            )
            
        except Exception as e:
            plt.close(fig)  # Clean up even on error
            logger.error(f"Error saving matplotlib figure: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def _create_error_result(self, chart_type: str, error_message: str) -> VisualizationResult:
        """Create error result"""
        return VisualizationResult(
            chart_type=chart_type,
            title="Error",
            file_path=None,
            html_content=None,
            base64_image=None,
            interactive_url=None,
            metadata={'renderer': 'matplotlib'},
            generation_timestamp=datetime.now().isoformat(),
            success=False,
            error_message=error_message
        )


class PlotlyVisualizer:
    """Creates interactive visualizations using Plotly"""
    
    def __init__(self):
        # Set default template
        pio.templates.default = "plotly_white"
    
    def create_line_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive line chart"""
        try:
            fig = go.Figure()
            
            x_col = df.columns[0]
            y_cols = df.columns[1:]
            
            for y_col in y_cols:
                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(width=3),
                    marker=dict(size=6)
                ))
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                xaxis_title=config.x_label or x_col,
                yaxis_title=config.y_label or 'Values',
                width=config.width,
                height=config.height,
                hovermode='x unified'
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly line chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_bar_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive bar chart"""
        try:
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df[x_col],
                    y=df[y_col],
                    text=df[y_col],
                    textposition='auto',
                    marker_color='steelblue'
                )
            ])
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                xaxis_title=config.x_label or x_col,
                yaxis_title=config.y_label or y_col,
                width=config.width,
                height=config.height
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly bar chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_histogram(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive histogram"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            data_col = numeric_cols[0]
            
            fig = go.Figure(data=[
                go.Histogram(
                    x=df[data_col].dropna(),
                    nbinsx=30,
                    marker_color='lightblue',
                    opacity=0.7
                )
            ])
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                xaxis_title=config.x_label or data_col,
                yaxis_title=config.y_label or 'Frequency',
                width=config.width,
                height=config.height
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly histogram: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_scatter_plot(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive scatter plot"""
        try:
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            # Color by third column if available
            if len(df.columns) > 2:
                c_col = df.columns[2]
                fig = px.scatter(df, x=x_col, y=y_col, color=c_col,
                               title=config.title, width=config.width, height=config.height)
            else:
                fig = px.scatter(df, x=x_col, y=y_col,
                               title=config.title, width=config.width, height=config.height)
            
            fig.update_layout(
                xaxis_title=config.x_label or x_col,
                yaxis_title=config.y_label or y_col
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly scatter plot: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_pie_chart(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive pie chart"""
        try:
            labels_col = df.columns[0]
            values_col = df.columns[1]
            
            # Aggregate data if needed
            pie_data = df.groupby(labels_col)[values_col].sum().reset_index()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=pie_data[labels_col],
                    values=pie_data[values_col],
                    hole=0.3,  # Donut style
                    textinfo='label+percent',
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                width=config.width,
                height=config.height
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly pie chart: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_heatmap(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create interactive heatmap"""
        try:
            numeric_df = df.select_dtypes(include=[np.number])
            corr_matrix = numeric_df.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                width=config.width,
                height=config.height
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating Plotly heatmap: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def create_3d_scatter(self, df: pd.DataFrame, config: ChartConfig) -> VisualizationResult:
        """Create 3D scatter plot"""
        try:
            if len(df.columns) < 3:
                raise ValueError("3D scatter plot requires at least 3 columns")
            
            x_col, y_col, z_col = df.columns[:3]
            
            fig = go.Figure(data=[go.Scatter3d(
                x=df[x_col],
                y=df[y_col],
                z=df[z_col],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df[z_col] if len(df.columns) > 3 else 'steelblue',
                    colorscale='Viridis',
                    opacity=0.8
                )
            )])
            
            fig.update_layout(
                title=dict(text=config.title, font=dict(size=16)),
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col
                ),
                width=config.width,
                height=config.height
            )
            
            return self._save_plotly_figure(fig, config)
            
        except Exception as e:
            logger.error(f"Error creating 3D scatter plot: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def _save_plotly_figure(self, fig: go.Figure, config: ChartConfig) -> VisualizationResult:
        """Save Plotly figure and return result"""
        try:
            # Generate HTML
            html_content = fig.to_html(include_plotlyjs=True, div_id="plotly-div")
            
            # Save to file if path specified
            file_path = None
            if config.save_path:
                if config.format == 'html':
                    file_path = config.save_path
                    fig.write_html(file_path)
                elif config.format == 'png':
                    file_path = config.save_path
                    fig.write_image(file_path)
                elif config.format == 'svg':
                    file_path = config.save_path
                    fig.write_image(file_path, format='svg')
            
            # Generate base64 image for embedding (with fallback)
            base64_image = None
            try:
                img_bytes = fig.to_image(format="png", width=config.width, height=config.height)
                base64_image = base64.b64encode(img_bytes).decode()
            except Exception as e:
                # Kaleido not available - this is optional for functionality
                logger.debug(f"Base64 image generation skipped (optional): {e}")
                # The chart still works as HTML, just no base64 embedding
            
            return VisualizationResult(
                chart_type=config.chart_type,
                title=config.title,
                file_path=file_path,
                html_content=html_content,
                base64_image=base64_image,
                interactive_url=None,
                metadata={'renderer': 'plotly', 'format': config.format},
                generation_timestamp=datetime.now().isoformat(),
                success=True,
                error_message=None
            )
            
        except Exception as e:
            logger.error(f"Error saving Plotly figure: {e}")
            return self._create_error_result(config.chart_type, str(e))
    
    def _create_error_result(self, chart_type: str, error_message: str) -> VisualizationResult:
        """Create error result"""
        return VisualizationResult(
            chart_type=chart_type,
            title="Error",
            file_path=None,
            html_content=None,
            base64_image=None,
            interactive_url=None,
            metadata={'renderer': 'plotly'},
            generation_timestamp=datetime.now().isoformat(),
            success=False,
            error_message=error_message
        )


class DataVisualizationAPI:
    """Main API for data visualization"""
    
    def __init__(self, output_dir: str = "visualizations"):
        self.data_processor = DataProcessor()
        self.matplotlib_viz = MatplotlibVisualizer()
        self.plotly_viz = PlotlyVisualizer()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.supported_chart_types = [
            'line', 'bar', 'histogram', 'scatter', 'pie', 'heatmap', '3d_scatter'
        ]
        
        self.visualization_history = []
    
    async def create_visualization(self, 
                                 data_source: Union[str, Dict, List, pd.DataFrame],
                                 chart_type: str,
                                 title: str,
                                 interactive: bool = True,
                                 **kwargs) -> VisualizationResult:
        """Create a visualization from data"""
        try:
            # Validate chart type
            if chart_type not in self.supported_chart_types:
                raise ValueError(f"Unsupported chart type: {chart_type}. Supported: {self.supported_chart_types}")
            
            # Load and validate data
            df = self.data_processor.load_data(data_source)
            is_valid, validation_message = self.data_processor.validate_data(df, chart_type)
            
            if not is_valid:
                raise ValueError(f"Data validation failed: {validation_message}")
            
            # Prepare data
            df_prepared = self.data_processor.prepare_data(df, chart_type)
            
            # Create configuration
            config = ChartConfig(
                chart_type=chart_type,
                title=title,
                interactive=interactive,
                **kwargs
            )
            
            # Generate filename if save_path not provided
            if not config.save_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{chart_type}_{timestamp}.{'html' if interactive else 'png'}"
                config.save_path = str(self.output_dir / filename)
            
            # Choose visualizer based on interactivity preference
            if interactive and chart_type != '3d_scatter':
                # Use Plotly for interactive charts
                visualizer = self.plotly_viz
            elif chart_type == '3d_scatter':
                # 3D scatter only available in Plotly
                visualizer = self.plotly_viz
            else:
                # Use Matplotlib for static charts
                visualizer = self.matplotlib_viz
            
            # Create visualization
            method_name = f"create_{chart_type.replace('3d_', '')}"
            if chart_type == '3d_scatter':
                method_name = "create_3d_scatter"
            elif chart_type == 'scatter':
                method_name = "create_scatter_plot"
            
            if hasattr(visualizer, method_name):
                result = getattr(visualizer, method_name)(df_prepared, config)
            else:
                # Fallback to basic chart types
                if chart_type in ['line', 'bar', 'pie', 'histogram', 'heatmap']:
                    if chart_type == 'line':
                        result = visualizer.create_line_chart(df_prepared, config)
                    elif chart_type == 'bar':
                        result = visualizer.create_bar_chart(df_prepared, config)
                    elif chart_type == 'pie':
                        result = visualizer.create_pie_chart(df_prepared, config)
                    elif chart_type == 'histogram':
                        result = visualizer.create_histogram(df_prepared, config)
                    elif chart_type == 'heatmap':
                        result = visualizer.create_heatmap(df_prepared, config)
                    else:
                        raise ValueError(f"Chart type '{chart_type}' not implemented")
                else:
                    raise ValueError(f"Chart type '{chart_type}' not supported")
            
            # Add to history
            if result.success:
                self.visualization_history.append({
                    'timestamp': result.generation_timestamp,
                    'chart_type': chart_type,
                    'title': title,
                    'data_shape': df.shape,
                    'interactive': interactive,
                    'file_path': result.file_path
                })
            
            logger.info(f"Created {chart_type} visualization: {title}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return VisualizationResult(
                chart_type=chart_type,
                title=title,
                file_path=None,
                html_content=None,
                base64_image=None,
                interactive_url=None,
                metadata={},
                generation_timestamp=datetime.now().isoformat(),
                success=False,
                error_message=str(e)
            )
    
    async def create_dashboard(self, 
                             data_source: Union[str, Dict, List, pd.DataFrame],
                             chart_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a multi-chart dashboard"""
        try:
            dashboard_results = []
            
            for chart_config in chart_configs:
                result = await self.create_visualization(
                    data_source=data_source,
                    **chart_config
                )
                dashboard_results.append(result)
            
            # Create combined HTML dashboard if all charts are successful
            successful_results = [r for r in dashboard_results if r.success and r.html_content]
            
            if successful_results:
                dashboard_html = self._create_dashboard_html(successful_results)
                dashboard_path = self.output_dir / f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(dashboard_html)
                
                return {
                    'success': True,
                    'dashboard_path': str(dashboard_path),
                    'individual_results': [r.to_dict() for r in dashboard_results],
                    'dashboard_html': dashboard_html
                }
            else:
                return {
                    'success': False,
                    'error': 'No successful visualizations to create dashboard',
                    'individual_results': [r.to_dict() for r in dashboard_results]
                }
                
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            return {
                'success': False,
                'error': str(e),
                'individual_results': []
            }
    
    def _create_dashboard_html(self, results: List[VisualizationResult]) -> str:
        """Create combined HTML dashboard"""
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<title>ATLES Data Visualization Dashboard</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            ".chart-container { margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }",
            ".chart-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>ATLES Data Visualization Dashboard</h1>",
            f"<p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        ]
        
        for i, result in enumerate(results):
            html_parts.extend([
                f'<div class="chart-container">',
                f'<div class="chart-title">{result.title}</div>',
                result.html_content,
                '</div>'
            ])
        
        html_parts.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html_parts)
    
    async def get_sample_data(self, dataset_type: str = 'sales') -> pd.DataFrame:
        """Generate sample data for testing"""
        if dataset_type == 'sales':
            dates = pd.date_range('2023-01-01', periods=100, freq='D')
            data = {
                'Date': dates,
                'Sales': np.random.normal(1000, 200, 100).cumsum(),
                'Profit': np.random.normal(100, 50, 100).cumsum(),
                'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
            }
        elif dataset_type == 'performance':
            data = {
                'Metric': ['CPU Usage', 'Memory Usage', 'Disk I/O', 'Network', 'Response Time'],
                'Value': [65, 78, 45, 23, 120],
                'Threshold': [80, 85, 70, 90, 100]
            }
        elif dataset_type == 'correlation':
            np.random.seed(42)
            n = 100
            data = {
                'Variable_A': np.random.normal(0, 1, n),
                'Variable_B': np.random.normal(0, 1, n),
                'Variable_C': np.random.normal(0, 1, n),
            }
            # Add some correlation
            data['Variable_D'] = data['Variable_A'] * 0.7 + np.random.normal(0, 0.5, n)
        else:
            # Default random data
            data = {
                'X': range(50),
                'Y': np.random.randint(1, 100, 50),
                'Category': np.random.choice(['A', 'B', 'C'], 50)
            }
        
        return pd.DataFrame(data)
    
    def get_visualization_history(self) -> List[Dict[str, Any]]:
        """Get history of created visualizations"""
        return self.visualization_history.copy()
    
    def get_supported_chart_types(self) -> List[str]:
        """Get list of supported chart types"""
        return self.supported_chart_types.copy()


# Integration function for ATLES
async def create_chart_for_response(data: Union[str, Dict, List, pd.DataFrame], 
                                  chart_type: str, 
                                  title: str,
                                  **kwargs) -> VisualizationResult:
    """
    ARCHITECTURAL FIX: This function enables ATLES to create actual, functional
    charts instead of providing non-functional example code.
    
    This should be called whenever the AI needs to create a visualization.
    """
    api = DataVisualizationAPI()
    return await api.create_visualization(data, chart_type, title, **kwargs)


# Test function
async def test_data_visualization():
    """Test the data visualization system"""
    print("📊 Testing Data Visualization System")
    print("=" * 50)
    
    try:
        api = DataVisualizationAPI()
        
        # Test 1: Line chart with sample data
        print("\n1. Creating line chart...")
        sales_data = await api.get_sample_data('sales')
        line_result = await api.create_visualization(
            data_source=sales_data,
            chart_type='line',
            title='Sales and Profit Over Time',
            interactive=True
        )
        print(f"Line chart: {'✅' if line_result.success else '❌'} - {line_result.error_message or 'Success'}")
        
        # Test 2: Bar chart
        print("\n2. Creating bar chart...")
        perf_data = await api.get_sample_data('performance')
        bar_result = await api.create_visualization(
            data_source=perf_data,
            chart_type='bar',
            title='System Performance Metrics',
            interactive=True
        )
        print(f"Bar chart: {'✅' if bar_result.success else '❌'} - {bar_result.error_message or 'Success'}")
        
        # Test 3: Correlation heatmap
        print("\n3. Creating heatmap...")
        corr_data = await api.get_sample_data('correlation')
        heatmap_result = await api.create_visualization(
            data_source=corr_data,
            chart_type='heatmap',
            title='Variable Correlation Matrix',
            interactive=True
        )
        print(f"Heatmap: {'✅' if heatmap_result.success else '❌'} - {heatmap_result.error_message or 'Success'}")
        
        # Test 4: Dashboard
        print("\n4. Creating dashboard...")
        dashboard_configs = [
            {'chart_type': 'line', 'title': 'Trends Over Time'},
            {'chart_type': 'bar', 'title': 'Performance Metrics'},
            {'chart_type': 'pie', 'title': 'Regional Distribution'}
        ]
        
        dashboard_result = await api.create_dashboard(sales_data, dashboard_configs)
        print(f"Dashboard: {'✅' if dashboard_result['success'] else '❌'}")
        
        # Show history
        history = api.get_visualization_history()
        print(f"\n📈 Created {len(history)} visualizations")
        
        print(f"\n💾 Output directory: {api.output_dir}")
        print("Files created:")
        for file in api.output_dir.glob("*"):
            print(f"  - {file.name}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_data_visualization())
