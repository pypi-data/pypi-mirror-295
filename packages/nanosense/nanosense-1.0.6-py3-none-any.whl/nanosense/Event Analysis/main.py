import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGroupBox, QLabel, QFileDialog,
                             QScrollArea, QMainWindow, QSizePolicy, QSplitter,
                             QRadioButton, QVBoxLayout, QLineEdit, QCheckBox, QDoubleSpinBox, QTabWidget,
                             QTableWidget, QTableWidgetItem, QSpinBox, QStyleFactory, QProgressDialog, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QPalette, QColor
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
import os

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class ScatterCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(ScatterCanvas, self).__init__(fig)

class SDAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SD Event Analysis App')
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Setup for the left panel (event categories and classifications)
        self.setup_left_panel()

        # Setup for the right panel (histograms, event plots, and event information)
        self.setup_right_panel()

        # Final layout setup
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.main_splitter)

        self.data = None
        self.events_data = {}
        self.classification_to_event_ids = {} 
        self.selected_event_ids = set() 

        # Add Save Analysis button
        self.save_analysis_button = QPushButton("Save Analysis")
        self.save_analysis_button.clicked.connect(self.save_analysis)
        self.top_group_layout.addWidget(self.save_analysis_button)



    def setup_left_panel(self):
        self.top_group = QGroupBox()
        self.top_group_layout = QVBoxLayout(self.top_group)
        
        # Setup components of top_group
        self.configure_top_group()

        # Setup scroll areas for Event Categories and Classifications
        self.event_categories_group_box, self.event_categories_layout = self.setup_scroll_area("Event Categories")
        self.event_classification_group_box, self.event_classification_layout = self.setup_scroll_area("Event Classifications")

        # Adjustments to place the Select All button at the bottom
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all_classifications)

        # Left Splitter Configuration
        self.left_splitter = QSplitter(Qt.Orientation.Vertical)
        self.left_splitter.addWidget(self.top_group)
        self.left_splitter.addWidget(self.event_categories_group_box)
        self.left_splitter.addWidget(self.event_classification_group_box)
        self.left_splitter.addWidget(self.select_all_button)  # Add the Select All button here
        self.left_splitter.setSizes([10, 300, 300, 50])  # Adjust sizes accordingly
        self.main_splitter.addWidget(self.left_splitter)

    def configure_top_group(self):
        self.title_label = QLabel('SD Event Analysis App')
        self.title_label.setFont(QFont('Arial', 23, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label = QLabel('shankar.dutt@anu.edu.au')
        self.subtitle_label.setFont(QFont('Arial', 15, QFont.Weight.Bold))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_group_layout.addWidget(self.title_label)
        self.top_group_layout.addWidget(self.subtitle_label)

        self.file_button = QPushButton('Select File')
        self.file_button.clicked.connect(self.load_file)
        self.top_group_layout.addWidget(self.file_button)

        # Container for Similarity Threshold Label and SpinBox
        self.threshold_container = QWidget()
        self.threshold_container_layout = QHBoxLayout(self.threshold_container)

        self.threshold_label = QLabel("Similarity Threshold: ")
        self.threshold_container_layout.addWidget(self.threshold_label)
        
        self.threshold_input = QDoubleSpinBox()
        self.threshold_input.setSuffix(" %")
        self.threshold_input.setRange(0, 100)
        self.threshold_input.setValue(90)
        self.threshold_input.setSingleStep(1)
        
        # Setup QTimer
        self.threshold_timer = QTimer(self)  # Create a QTimer instance
        self.threshold_timer.setSingleShot(True)  # Set the timer to single-shot mode
        self.threshold_timer.timeout.connect(self.on_threshold_changed)  # Connect the timer's timeout signal to on_threshold_changed
        self.threshold_input.valueChanged.connect(self.start_threshold_timer)  # Connect valueChanged signal to a method that starts the timer
        
        self.threshold_container_layout.addWidget(self.threshold_input)

        self.reclassify_checkbox = QCheckBox("Reclassify the event categories based on threshold")
        self.reclassify_checkbox.stateChanged.connect(self.on_threshold_changed)
        self.top_group_layout.addWidget(self.threshold_container)
        self.top_group_layout.addWidget(self.reclassify_checkbox)

    def start_threshold_timer(self):
        self.threshold_timer.start(500)  # Start/restart the timer with a 500ms delay

    def setup_right_panel(self):
        self.right_panel = QWidget()
        self.right_splitter = QSplitter(Qt.Orientation.Vertical)

        # Create tabs for histograms and scatter plots
        self.tabs = QTabWidget()
        self.histograms_tab = QWidget()
        self.scatter_plots_tab = QWidget()
        self.tabs.addTab(self.histograms_tab, "Histograms")
        self.tabs.addTab(self.scatter_plots_tab, "Scatter Plots")

        # Setup histograms tab
        self.setup_histograms_tab()

        # Setup scatter plots tab
        self.setup_scatter_plots_tab()

        self.right_splitter.addWidget(self.tabs)

        # Histograms group setup
        self.histograms_group = QGroupBox("Histograms")
        self.histograms_horizontal_layout = QHBoxLayout(self.histograms_group)
        
        
        # Adjusted setup for event plots and event information to be side by side
        self.bottom_right_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Event plots group setup
        self.event_plots_group = QGroupBox("Event Plots")
        self.event_plots_layout = QVBoxLayout(self.event_plots_group)
        self.event_plot_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.event_plots_layout.addWidget(self.event_plot_canvas)
        self.event_plot_toolbar = NavigationToolbar2QT(self.event_plot_canvas, self.event_plots_group)
        self.event_plot_toolbar.setIconSize(QSize(16, 16))
        self.event_plots_layout.addWidget(self.event_plot_toolbar)

        # Navigation controls under the event plots
        self.event_navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.event_navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.event_navigation_layout.addWidget(self.next_button)
        self.event_plots_layout.addLayout(self.event_navigation_layout)
        self.next_button.clicked.connect(self.next_event)  # Connect to the method handling the next event action
        self.prev_button.clicked.connect(self.previous_event)  # Connect to the method handling the previous event action


        self.bottom_right_splitter.addWidget(self.event_plots_group)

        # Event information group setup
        self.table_group = QGroupBox("Event Information")
        self.table_layout = QVBoxLayout(self.table_group)
        self.event_info_table = QTableWidget(10, 3)  # Adjust row, column count as needed
        self.event_info_table.setHorizontalHeaderLabels(['Type', 'Value', 'Description'])
        self.table_layout.addWidget(self.event_info_table)
        self.bottom_right_splitter.addWidget(self.table_group)

        self.right_splitter.addWidget(self.bottom_right_splitter)
        self.main_splitter.addWidget(self.right_splitter)

        # Setting initial sizes for splitters
        self.main_splitter.setSizes([300, 800])  # Adjust as needed
        self.right_splitter.setSizes([400, 350])  # Adjust as needed
        self.bottom_right_splitter.setSizes([400, 400])  # Adjust as needed

    def setup_histograms_tab(self):
        self.histograms_layout = QVBoxLayout(self.histograms_tab)
        self.histograms_group = QGroupBox("Histograms")
        self.histograms_horizontal_layout = QHBoxLayout(self.histograms_group)
        
        # Create and setup the first histogram canvas and toolbar for all events
        self.all_events_layout = QVBoxLayout()
        self.all_events_histogram_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.all_events_layout.addWidget(self.all_events_histogram_canvas)
        self.all_events_histogram_toolbar = NavigationToolbar2QT(self.all_events_histogram_canvas, self.histograms_group)
        self.all_events_histogram_toolbar.setIconSize(QSize(16, 16))
        self.all_events_layout.addWidget(self.all_events_histogram_toolbar)
        self.histograms_horizontal_layout.addLayout(self.all_events_layout)
        
        # Create and setup the second histogram canvas and toolbar for selected classifications
        self.selected_classifications_layout = QVBoxLayout()
        self.selected_classifications_histogram_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.selected_classifications_layout.addWidget(self.selected_classifications_histogram_canvas)
        self.selected_classifications_histogram_toolbar = NavigationToolbar2QT(self.selected_classifications_histogram_canvas, self.histograms_group)
        self.selected_classifications_histogram_toolbar.setIconSize(QSize(16, 16))
        self.selected_classifications_layout.addWidget(self.selected_classifications_histogram_toolbar)
        self.histograms_horizontal_layout.addLayout(self.selected_classifications_layout)
        
        self.histograms_layout.addWidget(self.histograms_group)

    def setup_scatter_plots_tab(self):
        self.scatter_plots_layout = QVBoxLayout(self.scatter_plots_tab)
        self.scatter_plots_group = QGroupBox("Scatter Plots")
        self.scatter_plots_horizontal_layout = QHBoxLayout(self.scatter_plots_group)

        # Create and setup the first scatter plot canvas and toolbar for all events
        self.all_events_scatter_layout = QVBoxLayout()
        self.all_events_scatter_canvas = ScatterCanvas(self, width=5, height=3)
        self.all_events_scatter_layout.addWidget(self.all_events_scatter_canvas)
        self.all_events_scatter_toolbar = NavigationToolbar2QT(self.all_events_scatter_canvas, self.scatter_plots_group)
        self.all_events_scatter_toolbar.setIconSize(QSize(16, 16))
        self.all_events_scatter_layout.addWidget(self.all_events_scatter_toolbar)
        self.scatter_plots_horizontal_layout.addLayout(self.all_events_scatter_layout)

        # Create and setup the second scatter plot canvas and toolbar for selected classifications
        self.selected_classifications_scatter_layout = QVBoxLayout()
        self.selected_classifications_scatter_canvas = ScatterCanvas(self, width=5, height=3)
        self.selected_classifications_scatter_layout.addWidget(self.selected_classifications_scatter_canvas)
        self.selected_classifications_scatter_toolbar = NavigationToolbar2QT(self.selected_classifications_scatter_canvas, self.scatter_plots_group)
        self.selected_classifications_scatter_toolbar.setIconSize(QSize(16, 16))
        self.selected_classifications_scatter_layout.addWidget(self.selected_classifications_scatter_toolbar)
        self.scatter_plots_horizontal_layout.addLayout(self.selected_classifications_scatter_layout)

        self.scatter_plots_layout.addWidget(self.scatter_plots_group)


    def setup_scroll_area(self, title):
        scroll_area = QScrollArea()  # Create the scroll area
        scroll_area.setWidgetResizable(True)
        
        container_widget = QWidget()  
        layout = QVBoxLayout(container_widget) 
        
        scroll_area.setWidget(container_widget) 

        group_box = QGroupBox(title)
        group_layout = QVBoxLayout(group_box)  
        group_layout.addWidget(scroll_area) 

        return group_box, layout 

    def on_threshold_changed(self):
        if self.data is not None:
            self.prepare_and_display_event_data()
            # Update all displayed information
            self.plot_all_events_histogram()
            self.plot_all_events_scatter()
            if self.selected_event_ids:
                self.plot_selected_events_histogram()
                self.plot_selected_events_scatter()
            # Re-display the current event if there is one
            if hasattr(self, 'current_event_index') and self.selected_event_ids:
                event_id = sorted(self.selected_event_ids)[self.current_event_index]
                self.plot_event_data(event_id)
                self.display_segment_info(event_id)

            # Clear and rebuild the event categories
            self.clear_layout(self.event_categories_layout)
            for category in sorted(self.events_data, key=lambda x: int(x.split()[0])):
                events_data = self.events_data[category]
                radio_button = QRadioButton(f"{category} ({len(events_data)} events)")
                radio_button.category = category
                radio_button.toggled.connect(self.on_radio_button_toggled)
                self.event_categories_layout.addWidget(radio_button)

            # Select the first category by default
            if self.event_categories_layout.count() > 0:
                self.event_categories_layout.itemAt(0).widget().setChecked(True)

    
    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open NPZ File', '', 'NPZ Files (*event_fitting.npz)')
        if file_name:
            self.data = np.load(file_name, allow_pickle=True)  # Directly load and store data
            self.prepare_and_display_event_data()

    def prepare_and_display_event_data(self):
        if self.data is not None:
            self.events_data.clear()
            self.clear_layout(self.event_categories_layout)
            self.clear_layout(self.event_classification_layout)
            self.plot_all_events_histogram()

            for key in self.data.files:
                if 'SEGMENT_INFO' in key and 'number_of_segments' in key:
                    event_id = int(key.split('_')[2])
                    mean_diffs_key = f'SEGMENT_INFO_{event_id}_segment_mean_diffs'
                    segment_widths_key = f'SEGMENT_INFO_{event_id}_segment_widths_time'
                    if mean_diffs_key in self.data and segment_widths_key in self.data:
                        mean_diffs = self.data[mean_diffs_key]
                        segment_widths = self.data[segment_widths_key]
                        original_classification, new_classification, final_classification, new_segment_count, original_segment_count, merged_segments = self.classify_event(mean_diffs)
                        
                        # Use new_segment_count for categorization only if reclassification is checked
                        category = f"{new_segment_count if self.reclassify_checkbox.isChecked() else original_segment_count} segments"
                        
                        self.events_data.setdefault(category, []).append((event_id, mean_diffs, segment_widths, 
                                                                        original_classification, new_classification, 
                                                                        final_classification, new_segment_count, 
                                                                        original_segment_count, merged_segments))
                    else:
                        original_segment_count = int(self.data[key][0])
                        category = f"{original_segment_count} segments"
                        self.events_data.setdefault(category, []).append((event_id, [], [], '', '', '', 
                                                                        original_segment_count, original_segment_count, []))

            for category in sorted(self.events_data, key=lambda x: int(x.split()[0])):
                events_data = self.events_data[category]
                radio_button = QRadioButton(f"{category} ({len(events_data)} events)")
                radio_button.category = category
                radio_button.toggled.connect(self.on_radio_button_toggled)
                self.event_categories_layout.addWidget(radio_button)

            if self.event_categories_layout.count() > 0:
                self.event_categories_layout.itemAt(0).widget().setChecked(True)

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.update_classification_group(radio_button.category)

    def update_classification_group(self, category):
        self.clear_layout(self.event_classification_layout)
        classification_counts = {}
        self.classification_checkboxes = []
        self.classification_to_event_ids.clear()  # Reset the mapping

        for event_data in self.events_data.get(category, []):
            event_id, _, _, original_classification, new_classification, final_classification, new_segment_count, _, merged_segments = event_data
            
            if self.reclassify_checkbox.isChecked() and original_classification != final_classification:
                display_classification = f"{original_classification} -> {final_classification}"
                classification_key = f"{original_classification} -> {final_classification}"
            else:
                display_classification = original_classification
                classification_key = original_classification
            
            # Create the display string with underlined merged segments
            display_string = ""
            for i, char in enumerate(final_classification if self.reclassify_checkbox.isChecked() else original_classification):
                if self.reclassify_checkbox.isChecked() and merged_segments[i]:
                    display_string += f"<u>{char}</u>"
                else:
                    display_string += char
            
            if self.reclassify_checkbox.isChecked() and original_classification != final_classification:
                display_string = f"{original_classification} -> {display_string}"
            
            classification_counts[classification_key] = classification_counts.get(classification_key, 0) + 1
            
            if classification_key not in self.classification_to_event_ids:
                self.classification_to_event_ids[classification_key] = []
            self.classification_to_event_ids[classification_key].append(event_id)

        for classification_key, count in sorted(classification_counts.items(), key=lambda x: x[0]):
            checkbox = QCheckBox(f"Category {classification_key} ({count} events)")
            checkbox.classification = classification_key
            checkbox.stateChanged.connect(self.on_checkbox_state_changed)
            self.event_classification_layout.addWidget(checkbox)
            self.classification_checkboxes.append(checkbox)

        # Ensure the "Select All" button works with the newly added checkboxes
        self.select_all_button.clicked.disconnect()
        self.select_all_button.clicked.connect(self.select_all_classifications)

    def classify_event(self, mean_diffs):
        original_segment_count = len(mean_diffs)
        merged_segments = [False] * original_segment_count
        
        def get_label(index):
            return str(index + 1) if index < 9 else chr(ord('A') + index - 9)

        # Original classification
        sorted_indices = np.argsort(np.abs(mean_diffs))
        original_classifications = [''] * original_segment_count
        for i, idx in enumerate(sorted_indices):
            original_classifications[idx] = get_label(i)
        
        if self.reclassify_checkbox.isChecked():
            threshold_ratio = self.threshold_input.value() / 100.0
            
            # Reclassification
            new_classifications = [get_label(0)]
            merged_mean_diffs = [mean_diffs[0]]

            for i in range(1, original_segment_count):
                prev_mean_diff = merged_mean_diffs[-1]
                current_mean_diff = mean_diffs[i]
                lower_bound = prev_mean_diff - abs(prev_mean_diff) * (1 - threshold_ratio)
                upper_bound = prev_mean_diff + abs(prev_mean_diff) * (1 - threshold_ratio)
                
                if lower_bound <= current_mean_diff <= upper_bound:
                    new_classifications.append(new_classifications[-1])
                    merged_segments[i] = True
                    # Update the mean diff for the merged segment
                    merged_mean_diffs[-1] = (merged_mean_diffs[-1] * new_classifications.count(new_classifications[-1]) + current_mean_diff) / (new_classifications.count(new_classifications[-1]) + 1)
                else:
                    new_classifications.append(get_label(len(set(new_classifications))))
                    merged_mean_diffs.append(current_mean_diff)

            # Rename new classifications based on merged mean_diff values
            unique_classifications = sorted(set(new_classifications))
            sorted_merged_diffs = sorted(set(zip(unique_classifications, merged_mean_diffs)), key=lambda x: x[1])
            new_classification_to_final = {class_: get_label(i) for i, (class_, _) in enumerate(sorted_merged_diffs)}
            
            final_classifications = [new_classification_to_final[c] for c in new_classifications]
            new_segment_count = len(set(final_classifications))
        else:
            new_classifications = original_classifications
            final_classifications = original_classifications
            new_segment_count = original_segment_count
            merged_segments = [False] * original_segment_count

        # Create the final classification strings
        original_classification_string = ''.join(original_classifications)
        new_classification_string = ''.join(new_classifications)
        final_classification_string = ''.join(final_classifications)

        return (original_classification_string, new_classification_string, 
                final_classification_string, new_segment_count, 
                original_segment_count, merged_segments)

    def plot_selected_events_scatter(self):
        all_mean_diffs = []
        all_segment_widths = []
        for event_id in self.selected_event_ids:
            for segment_count, events in self.events_data.items():
                for event_data in events:
                    if event_data[0] == event_id:
                        _, mean_diffs, segment_widths, *_ = event_data  # Unpack only the needed values
                        all_mean_diffs.extend(mean_diffs)
                        all_segment_widths.extend(segment_widths)
                        break

        if len(all_mean_diffs) > 0 and len(all_segment_widths) > 0:
            # Clear the figure/canvas before plotting
            self.selected_classifications_scatter_canvas.figure.clear()

            ax = self.selected_classifications_scatter_canvas.figure.subplots()
            ax.scatter(np.log(np.array(all_segment_widths)*1e3), all_mean_diffs)
            ax.set_title('Segment Mean Diffs vs log(dt (ms)) for Selected Events')
            ax.set_xlabel('log(Δt (ms))')
            ax.set_ylabel('Mean Diff')
            self.selected_classifications_scatter_canvas.figure.tight_layout()
            self.selected_classifications_scatter_canvas.draw()


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def select_all_classifications(self):
        try:
            if any(not checkbox.isChecked() for checkbox in self.classification_checkboxes):
                for checkbox in self.classification_checkboxes:
                    checkbox.setChecked(True)
            else:
                for checkbox in self.classification_checkboxes:
                    checkbox.setChecked(False)

            # Update the button text based on the new state
            self.select_all_button.setText("Unselect All" if any(checkbox.isChecked() for checkbox in self.classification_checkboxes) else "Select All")
        except:
            pass


    def plot_all_events_histogram(self):
        max_mean_diffs = []
        for key in self.data.files:
            if 'segment_mean_diffs' in key:
                mean_diffs = self.data[key]
                max_mean_diffs.append(np.max(mean_diffs))
        
        # Clear the figure/canvas before plotting
        self.all_events_histogram_canvas.figure.clear()

        ax = self.all_events_histogram_canvas.figure.subplots()
        
        # Calculate bin edges with 'auto' and then double the number of bins
        _, bins_auto = np.histogram(max_mean_diffs, bins='auto')
        num_bins_auto = len(bins_auto) - 1  # Number of bins is one less than the number of edges
        doubled_num_bins = num_bins_auto * 2  # Double the number of bins
        
        # Use linspace to create new bin edges with doubled number of bins
        new_bins = np.linspace(bins_auto[0], bins_auto[-1], doubled_num_bins + 1)
        
        ax.hist(max_mean_diffs, bins=new_bins)
        ax.set_title('Max Segment Mean Diffs for All Events')
        ax.set_xlabel('Max Mean Diff')
        ax.set_ylabel('Frequency')
        self.all_events_histogram_canvas.figure.tight_layout()
        self.all_events_histogram_canvas.draw()
        # Plot the corresponding scatter plot
        self.plot_all_events_scatter()

    def on_checkbox_state_changed(self):
        self.selected_event_ids.clear()  # Clear and repopulate based on current selections

        for checkbox in self.classification_checkboxes:
            if checkbox.isChecked():
                # Add all event IDs from this classification to the selected set
                event_ids = self.classification_to_event_ids.get(checkbox.classification, [])
                self.selected_event_ids.update(event_ids)
        
        # Plot and display segment info for the first selected event, if any
        self.current_event_index = 0
        if self.selected_event_ids:
            first_event_id = next(iter(sorted(self.selected_event_ids)))
            self.plot_event_data(first_event_id)
            self.display_segment_info(first_event_id)

        # Update plots/information here
        self.plot_selected_events_histogram()
        self.plot_selected_events_scatter()
    
    def setup_navigation_buttons(self):
        self.current_event_index = 0  # Initialize the current index
        self.previous_button.clicked.connect(self.previous_event)
        self.next_button.clicked.connect(self.next_event)

    def previous_event(self):
        if self.selected_event_ids and self.current_event_index > 0:
            self.current_event_index -= 1
            event_id = sorted(self.selected_event_ids)[self.current_event_index]
            self.plot_event_data(event_id)
            self.display_segment_info(event_id)

    def next_event(self):
        if self.selected_event_ids and self.current_event_index < len(self.selected_event_ids) - 1:
            self.current_event_index += 1
            event_id = sorted(self.selected_event_ids)[self.current_event_index]
            self.plot_event_data(event_id)
            self.display_segment_info(event_id)

    def plot_selected_events_histogram(self):
        all_mean_diffs = []
        for event_id in self.selected_event_ids:
            key = f'SEGMENT_INFO_{event_id}_segment_mean_diffs'
            if key in self.data:
                mean_diffs = self.data[key]
                all_mean_diffs.extend(mean_diffs)              
        
        if len(all_mean_diffs)>1:
            # Clear the figure/canvas before plotting
            self.selected_classifications_histogram_canvas.figure.clear()

            ax = self.selected_classifications_histogram_canvas.figure.subplots()
            
            # Decide on the number of bins
            num_bins = 'auto'  # Default
            
            # Plot the histogram with bar boundaries
            ax.hist(all_mean_diffs, bins=num_bins, edgecolor='black')

            ax.set_title('Segment Mean Diffs for Selected Events')
            ax.set_xlabel('Mean Diff')
            ax.set_ylabel('Frequency')
            self.selected_classifications_histogram_canvas.figure.tight_layout()
            self.selected_classifications_histogram_canvas.draw()
        
        # Plot the corresponding scatter plot
        self.plot_selected_events_scatter()

    def plot_all_events_scatter(self):
        max_mean_diffs = []
        event_widths = []
        for key in self.data.files:
            if 'segment_mean_diffs' in key:
                mean_diffs = self.data[key]
                max_mean_diffs.append(np.max(mean_diffs))

            if 'event_width' in key:
                event_widths.append(self.data[key])

        if len(max_mean_diffs) > 0 and len(event_widths) > 0:
            # Clear the figure/canvas before plotting
            self.all_events_scatter_canvas.figure.clear()

            ax = self.all_events_scatter_canvas.figure.subplots()
            ax.scatter(np.log(np.array(event_widths)*1e3), max_mean_diffs)
            ax.set_title('Max Segment Mean Diffs vs log(Event Width) for All Events')
            ax.set_xlabel('log(Δt (ms))')
            ax.set_ylabel('ΔI')
            self.all_events_scatter_canvas.figure.tight_layout()
            self.all_events_scatter_canvas.draw()

    def plot_event_data(self, event_id):
        # Retrieve event data
        x_values = self.data[f'EVENT_DATA_{event_id}_part_0']
        y_values_event = self.data[f'EVENT_DATA_{event_id}_part_1']
        y_values_fit = self.data[f'EVENT_DATA_{event_id}_part_3']
        
        # Clear the plot
        self.event_plot_canvas.figure.clear()
        
        # Create a new plot
        ax = self.event_plot_canvas.figure.subplots()
        ax.plot(x_values, y_values_event, label='Event Data')
        ax.plot(x_values, y_values_fit, label='Fit Data', linestyle='--')
        
        # Adding legends, title, and labels
        ax.legend()
        ax.set_title(f'Event {event_id} Data')
        ax.set_xlabel('Time')
        ax.set_ylabel('Data')
        
        self.event_plot_canvas.figure.tight_layout()
        # Refresh the canvas
        self.event_plot_canvas.draw()

    

    def display_segment_info(self, event_id):
        for category, events in self.events_data.items():
            for event in events:
                if event[0] == event_id:
                    original_segment_count = event[7]
                    segment_mean_diffs = event[1]
                    segment_widths_time = event[2]
                    merged_segments = event[8]
                    break
            else:
                continue
            break
        
        self.event_info_table.setRowCount(original_segment_count)
        self.event_info_table.setColumnCount(3)
        self.event_info_table.setHorizontalHeaderLabels(['Segment', 'Mean Diff', 'Width Time'])
        
        for i in range(original_segment_count):
            segment_item = QTableWidgetItem(f"{i + 1}")
            mean_diff_item = QTableWidgetItem(f"{segment_mean_diffs[i]:.3g}")
            width_time_item = QTableWidgetItem(f"{segment_widths_time[i]:.3g}")
            
            if self.reclassify_checkbox.isChecked() and merged_segments[i]:
                font = segment_item.font()
                font.setUnderline(True)
                segment_item.setFont(font)
                mean_diff_item.setFont(font)
                width_time_item.setFont(font)
            
            self.event_info_table.setItem(i, 0, segment_item)
            self.event_info_table.setItem(i, 1, mean_diff_item)
            self.event_info_table.setItem(i, 2, width_time_item)

        self.event_info_table.resizeColumnsToContents()
        self.event_info_table.resizeRowsToContents()


    def save_analysis(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load data before saving analysis.")
            return

        try:
            # Ask for the directory to save files
            save_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Analysis")
            if not save_dir:
                return  # User cancelled the dialog

            # Ask for the CSV file name
            csv_name, ok = QInputDialog.getText(self, "CSV File Name", "Enter the name for the CSV file (without .csv):")
            if not ok or not csv_name:
                return  # User cancelled or didn't enter a name

            # Create progress dialog
            progress = QProgressDialog("Saving analysis...", "Cancel", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("Save Progress")
            progress.show()

            # Create a folder for plots
            plots_dir = os.path.join(save_dir, "plots")
            os.makedirs(plots_dir, exist_ok=True)

            # Save CSV
            self.save_csv(progress, save_dir, csv_name)

            # Save plots
            self.save_plots(progress, plots_dir)

            progress.setValue(100)
            QMessageBox.information(self, "Save Complete", "Analysis has been saved successfully.")
        except Exception as e:
            error_msg = f"An error occurred while saving the analysis: {str(e)}"
            print(error_msg)  # Print to console for debugging
            QMessageBox.critical(self, "Error", error_msg)

    def save_csv(self, progress, save_dir, csv_name):
        file_name = os.path.join(save_dir, f"{csv_name}.csv")
        
        total_events = sum(len(events) for events in self.events_data.values())
        
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Category', 'Number of Events', 'Percentage', 'Classifications', 'Number of Events', 'Percentage within Category', 'Percentage of Total Events'])

            row_count = sum(1 for _ in self.events_data.items())
            for i, (segment_count, events) in enumerate(self.events_data.items()):
                category_events = len(events)
                category_percentage = (category_events / total_events) * 100
                
                # Write category row
                writer.writerow([
                    f"{segment_count} segments",
                    category_events,
                    f"{category_percentage:.2f}%",
                    "", "", "", ""  # Empty cells for classifications
                ])

                # Write classification rows
                classifications = {}
                for event in events:
                    if self.reclassify_checkbox.isChecked() and event[3] != event[5]:
                        classification_key = f"{event[3]} -> {event[5]}"
                    else:
                        classification_key = event[3]
                    classifications[classification_key] = classifications.get(classification_key, 0) + 1

                for classification, count in classifications.items():
                    writer.writerow([
                        "", "", "",  # Empty cells for category
                        classification,
                        count,
                        f"{(count/category_events)*100:.2f}%",
                        f"{(count/total_events)*100:.2f}%"
                    ])

                progress.setValue(int((i + 1) / row_count * 50))  # CSV saving is 50% of the progress


    def save_plots(self, progress, plots_dir):
        # Save all events histogram and scatter plot
        self.save_figure(self.all_events_histogram_canvas, os.path.join(plots_dir, "all_events_histogram.png"))
        self.save_figure(self.all_events_scatter_canvas, os.path.join(plots_dir, "all_events_scatter.png"))

        # Save selected events histogram and scatter plot
        self.save_figure(self.selected_classifications_histogram_canvas, os.path.join(plots_dir, "selected_events_histogram.png"))
        self.save_figure(self.selected_classifications_scatter_canvas, os.path.join(plots_dir, "selected_events_scatter.png"))

        # Save individual category and classification plots
        total_categories = len(self.events_data)
        total_classifications = sum(len(set(event[3] for event in events)) for events in self.events_data.values())
        total_items = total_categories + total_classifications
        
        current_item = 0

        for segment_count, events in self.events_data.items():
            category_dir = os.path.join(plots_dir, f"category_{segment_count}_segments")
            os.makedirs(category_dir, exist_ok=True)

            # Plot for the entire category
            self.plot_category_histogram(segment_count, events)
            self.save_figure(plt.gcf(), os.path.join(category_dir, f"category_{segment_count}_segments_histogram.png"))
            plt.close()

            self.plot_category_scatter(segment_count, events)
            self.save_figure(plt.gcf(), os.path.join(category_dir, f"category_{segment_count}_segments_scatter.png"))
            plt.close()

            current_item += 1
            progress.setValue(int(50 + (current_item / total_items) * 50))

            # Plots for each classification within the category
            classifications = set(event[3] for event in events)
            for classification in classifications:
                classification_events = [event for event in events if event[3] == classification]
                
                self.plot_classification_histogram(classification, [event[0] for event in classification_events])
                self.save_figure(plt.gcf(), os.path.join(category_dir, f"classification_{classification}_histogram.png"))
                plt.close()

                self.plot_classification_scatter(classification, [event[0] for event in classification_events])
                self.save_figure(plt.gcf(), os.path.join(category_dir, f"classification_{classification}_scatter.png"))
                plt.close()

                current_item += 1
                progress.setValue(int(50 + (current_item / total_items) * 50))

    def save_figure(self, canvas, filename):
        if isinstance(canvas, FigureCanvas):
            canvas.figure.savefig(filename)
        elif isinstance(canvas, plt.Figure):
            canvas.savefig(filename)
        else:
            print(f"Unsupported figure type for {filename}")


    def plot_classification_histogram(self, classification, event_ids):
        all_mean_diffs = []
        for event_id in event_ids:
            key = f'SEGMENT_INFO_{event_id}_segment_mean_diffs'
            if key in self.data:
                mean_diffs = self.data[key]
                all_mean_diffs.extend(mean_diffs)

        plt.figure()
        plt.hist(all_mean_diffs, bins='auto', edgecolor='black')
        plt.title(f'Segment Mean Diffs for Classification {classification}\n(Events: {len(event_ids)})')
        plt.xlabel('Mean Diff')
        plt.ylabel('Frequency')

    def plot_classification_scatter(self, classification, event_ids):
        max_mean_diffs = []
        event_widths = []
        missing_data_count = 0
        data_keys = set(self.data.keys())

        #print(f"Attempting to plot data for classification {classification} with {len(event_ids)} events")
        #print(f"Total number of keys in self.data: {len(data_keys)}")

        for event_id in event_ids:
            mean_diffs_key = f'SEGMENT_INFO_{event_id}_segment_mean_diffs'
            segment_widths_key = f'SEGMENT_INFO_{event_id}_segment_widths_time'
            
            if mean_diffs_key in self.data and segment_widths_key in self.data:
                mean_diffs = self.data[mean_diffs_key]
                segment_widths = self.data[segment_widths_key]
                if len(mean_diffs) > 0 and len(segment_widths) > 0:
                    max_mean_diffs.append(np.max(np.abs(mean_diffs)))
                    event_widths.append(np.sum(segment_widths))  # Calculate total event width
                else:
                    missing_data_count += 1
                    print(f"Warning: Empty data for event_id {event_id}")
            else:
                missing_data_count += 1
                print(f"Warning: Missing data for event_id {event_id}")
                print(f"Keys not found: {mean_diffs_key if mean_diffs_key not in self.data else ''}, "
                    f"{segment_widths_key if segment_widths_key not in self.data else ''}")
                
        if len(max_mean_diffs) > 0 and len(event_widths) > 0:
            plt.figure()
            plt.scatter(np.log(np.array(event_widths)*1e3), max_mean_diffs)
            plt.title(f'Max Segment Mean Diffs vs log(Event Width) for Classification {classification}\n'
                    f'(Events: {len(event_ids)}, Plotted: {len(max_mean_diffs)})')
            plt.xlabel('log(Δt (ms))')
            plt.ylabel('|ΔI|')
            if missing_data_count > 0:
                plt.figtext(0.5, 0.01, f"Warning: {missing_data_count} events had missing or invalid data",
                            wrap=True, horizontalalignment='center', fontsize=8)
        else:
            print(f"No data to plot for classification {classification}. "
                f"Total events: {len(event_ids)}, Missing data: {missing_data_count}")
            # Create a figure with just the warning text
            plt.figure()
            plt.text(0.5, 0.5, f"No data to plot for classification {classification}\n"
                            f"Total events: {len(event_ids)}, Missing data: {missing_data_count}", 
                    horizontalalignment='center', verticalalignment='center')
            plt.axis('off')

        # Print a separator for clarity in the console output
        #print("-" * 50)

    def plot_category_histogram(self, segment_count, events):
        all_mean_diffs = []
        for event in events:
            all_mean_diffs.extend(event[1])  # event[1] contains mean_diffs

        plt.figure()
        plt.hist(all_mean_diffs, bins='auto', edgecolor='black')
        plt.title(f'Segment Mean Diffs for Category: {segment_count} segments\n(Events: {len(events)})')
        plt.xlabel('Mean Diff')
        plt.ylabel('Frequency')

    def plot_category_scatter(self, segment_count, events):
        max_mean_diffs = [np.max(np.abs(event[1])) for event in events]  # event[1] contains mean_diffs
        event_widths = [np.sum(event[2]) for event in events]  # event[2] contains segment_widths

        plt.figure()
        plt.scatter(np.log(np.array(event_widths)*1e3), max_mean_diffs)
        plt.title(f'Max Segment Mean Diffs vs log(Event Width) for Category: {segment_count} segments\n(Events: {len(events)})')
        plt.xlabel('log(Δt (ms))')
        plt.ylabel('|ΔI|')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))  #
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    mainWin = SDAnalysisApp()
    mainWin.showMaximized()
    sys.exit(app.exec())
