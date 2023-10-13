import tkinter as tk
import tkinter.ttk as ttk
from core import*


### PREAMBLE ###
version = "1.0"
title = "S/C Link Margin Calculator"

### VALIDATION & CONDITIONAL DATA ENTRY FUNCTIONS ###
def validate_input(P):
    '''Data entry verification, only float valid'''
    try:
        float(P) if P else 0
        return True
    except ValueError:
        return False
    
def toggle_elong_angle_entry():
    '''Toggle functionality to elongation angle'''
    if (target_body_select.get() == "Earth") or (target_body_select.get() == "Moon"):
        elong_angle_entry.delete(0, 'end')  # Clear the input field
        elong_angle_entry.config(state="disabled")    
    else:
        elong_angle_entry.config(state="normal")

def toggle_efficiency_entry(entry, enabled_var):
    '''Toggle functionality to antenna efficiency'''
    if enabled_var.get():
        entry.config(state="normal")
    else:
        entry.delete(0, 'end')
        entry.insert(0, "0.55")
        entry.config(state="disabled")

def calculate_link_margin():
    '''Utilize core functions to generate link margin and output to UI'''
    link_margin_uplink = "OUTPUT"
    link_margin_downlink = "OUTPUT"
    link_margin_output_uplink.config(text=link_margin_uplink)
    link_margin_output_downlink.config(text=link_margin_downlink)

#### UI LAYOUT/SETUP ###
root = tk.Tk()
root.title(f"{title} v{version}")

# Set the window icon
icon = tk.PhotoImage(file="./img/icon.png")
root.iconphoto(False, icon)

# Set up data entry validation
vcmd = root.register(validate_input)

# Set up modulation/coding type options
target_body_options = ["Mercury",
                       "Venus",
                       "Earth",
                       "Moon",
                       "Mars",
                       "Jupiter",
                       "Saturn",
                       "Uranus",
                       "Neptune"]
target_body_select = tk.StringVar()
target_body_select.set(target_body_options[2])
target_body_select.trace_add("write", lambda *args: toggle_elong_angle_entry())


# Set up elongation angle input toggle
elong_angle_enabled = tk.BooleanVar()
elong_angle_enabled.set(False)

# Set up antenna efficiency input toggle
antenna_sc_eff_enabled = tk.BooleanVar()
antenna_sc_eff_enabled.set(False)

antenna_gs_eff_enabled = tk.BooleanVar()
antenna_gs_eff_enabled.set(False)


# Set up modulation/coding type options
modulation_coding_options = ["Uncoded",
                             "Reed-Solomon (only)",
                             "Convolutional: r=1/2",
                             "Convolutional-RS: r=1/2",
                             "Convolutional-RS: r=1/6",
                             "Turbo-Codes: r=1/2",
                             "Turbo-Codes: r=1/6",
                             "LDPC: r=3/4"]
selected_modulation_coding = tk.StringVar()
selected_modulation_coding.set(modulation_coding_options[0])

# Set up BER exponent options
BER_exponent = tk.StringVar()
BER_exponent.set("-6")

# Orbital target input field
target_body_label = tk.Label(root, text="Orbital target:")
target_body_label.grid(row=0, column=0)
target_body_option_menu = ttk.Combobox(root, textvariable=target_body_select, values=target_body_options, state="readonly", width=13)
target_body_option_menu.grid(row=0, column=1)

# S/C transmitter power input field
transmitter_sc_power_label = tk.Label(root, text="S/C transmitter power:")
transmitter_sc_power_label.grid(row=1, column=0)
transmitter_sc_power_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
transmitter_sc_power_entry.grid(row=1, column=1)
transmitter_sc_power_unit = tk.Label(root, text="[W]")
transmitter_sc_power_unit.grid(row=1, column=2)

# GS transmitter power input field
transmitter_gs_power_label = tk.Label(root, text="GS transmitter power:")
transmitter_gs_power_label.grid(row=2, column=0)
transmitter_gs_power_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
transmitter_gs_power_entry.grid(row=2, column=1)
transmitter_gs_power_unit = tk.Label(root, text="[W]")
transmitter_gs_power_unit.grid(row=2, column=2)

# Transmitter loss factor input field
transmitter_sc_LF_label = tk.Label(root, text="Transmitter loss factor:")
transmitter_sc_LF_label.grid(row=3, column=0)
transmitter_sc_LF_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
transmitter_sc_LF_entry.grid(row=3, column=1)
transmitter_sc_LF_unit = tk.Label(root, text="[-]")
transmitter_sc_LF_unit.grid(row=3, column=2)

# Receiver loss factor input field
receiver_sc_LF_label = tk.Label(root, text="Receiver loss factor:")
receiver_sc_LF_label.grid(row=4, column=0)
receiver_sc_LF_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
receiver_sc_LF_entry.grid(row=4, column=1)
receiver_sc_LF_unit = tk.Label(root, text="[-]")
receiver_sc_LF_unit.grid(row=4, column=2)

# Downlink frequency input field
downlink_freq_label = tk.Label(root, text="Downlink frequency:")
downlink_freq_label.grid(row=5, column=0)
downlink_freq_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
downlink_freq_entry.grid(row=5, column=1)
downlink_freq_unit = tk.Label(root, text="[GHz]")
downlink_freq_unit.grid(row=5, column=2)

# Turn around ratio (TAR) input field
sc_TAR_label = tk.Label(root, text="Turn around ratio:")
sc_TAR_label.grid(row=6, column=0)
sc_TAR_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
sc_TAR_entry.grid(row=6, column=1)
sc_TAR_unit = tk.Label(root, text="[-]")
sc_TAR_unit.grid(row=6, column=2)

# S/C antenna diameter input field
antenna_sc_diam_label = tk.Label(root, text="S/C antenna diameter:")
antenna_sc_diam_label.grid(row=7, column=0)
antenna_sc_diam_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
antenna_sc_diam_entry.grid(row=7, column=1)
antenna_sc_diam_unit = tk.Label(root, text="[m]")
antenna_sc_diam_unit.grid(row=7, column=2)

# S/C antenna efficiency input field
antenna_sc_eff_label = tk.Label(root, text="S/C antenna efficiency:")
antenna_sc_eff_label.grid(row=8, column=0)
antenna_sc_eff_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
antenna_sc_eff_entry.grid(row=8, column=1)
antenna_sc_eff_unit = tk.Label(root, text="[-]")
antenna_sc_eff_unit.grid(row=8, column=2)
antenna_sc_eff_checkbox = tk.Checkbutton(root, variable=antenna_sc_eff_enabled)
antenna_sc_eff_checkbox.grid(row=8, column=3)
antenna_sc_eff_enabled.trace_add("write", lambda *args: toggle_efficiency_entry(antenna_sc_eff_entry, antenna_sc_eff_enabled))
toggle_efficiency_entry(antenna_sc_eff_entry, antenna_sc_eff_enabled)

# GS antenna diamter input field
antenna_gs_diam_label = tk.Label(root, text="GS antenna diameter:")
antenna_gs_diam_label.grid(row=9, column=0)
antenna_gs_diam_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
antenna_gs_diam_entry.grid(row=9, column=1)
antenna_gs_diam_unit = tk.Label(root, text="[m]")
antenna_gs_diam_unit.grid(row=9, column=2)

# GS antenna efficiency input field
antenna_gs_eff_label = tk.Label(root, text="GS antenna efficiency:")
antenna_gs_eff_label.grid(row=10, column=0)
antenna_gs_eff_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
antenna_gs_eff_entry.grid(row=10, column=1)
antenna_gs_eff_unit = tk.Label(root, text="[-]")
antenna_gs_eff_unit.grid(row=10, column=2)
antenna_gs_eff_checkbox = tk.Checkbutton(root, variable=antenna_gs_eff_enabled)
antenna_gs_eff_checkbox.grid(row=10, column=3)
antenna_gs_eff_enabled.trace_add("write", lambda *args: toggle_efficiency_entry(antenna_gs_eff_entry, antenna_gs_eff_enabled))
toggle_efficiency_entry(antenna_gs_eff_entry, antenna_gs_eff_enabled)

# Orbit altitude input field
orbit_alt_label = tk.Label(root, text="Orbit altitude:")
orbit_alt_label.grid(row=11, column=0)
orbit_alt_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
orbit_alt_entry.grid(row=11, column=1)
orbit_alt_unit = tk.Label(root, text="[km]")
orbit_alt_unit.grid(row=11, column=2)

# Elongation angle input field
elong_angle_label = tk.Label(root, text="Elongation angle:")
elong_angle_label.grid(row=12, column=0)
elong_angle_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13, state="disabled")
elong_angle_entry.grid(row=12, column=1)
elong_angle_unit = tk.Label(root, text="[°]")
elong_angle_unit.grid(row=12, column=2)
elong_angle_enabled.trace_add("write", lambda *args: toggle_elong_angle_entry())

# Pointing offset angle input field
pointing_offset_angle_label = tk.Label(root, text="Pointing offset angle:")
pointing_offset_angle_label.grid(row=13, column=0)
pointing_offset_angle_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
pointing_offset_angle_entry.grid(row=13, column=1)
pointing_offset_angle_unit = tk.Label(root, text="[°]")
pointing_offset_angle_unit.grid(row=13, column=2)

# Required uplink data rate input field
uplink_datarate_req_label = tk.Label(root, text="Required uplink data rate:")
uplink_datarate_req_label.grid(row=14, column=0)
uplink_datarate_req_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
uplink_datarate_req_entry.grid(row=14, column=1)
uplink_datarate_req_unit = tk.Label(root, text="[bit/s]")
uplink_datarate_req_unit.grid(row=14, column=2)

# Payload swath width angle input field
PL_SW_angle_label = tk.Label(root, text="Payload swath width angle:")
PL_SW_angle_label.grid(row=15, column=0)
PL_SW_angle_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
PL_SW_angle_entry.grid(row=15, column=1)
PL_SW_angle_unit = tk.Label(root, text="[deg]")
PL_SW_angle_unit.grid(row=15, column=2)

# Payload pixel size input field
PL_pixel_size_label = tk.Label(root, text="Payload pixel size:")
PL_pixel_size_label.grid(row=16, column=0)
PL_pixel_size_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
PL_pixel_size_entry.grid(row=16, column=1)
PL_pixel_size_unit = tk.Label(root, text="[arcmin]")
PL_pixel_size_unit.grid(row=16, column=2)

# Payload bits per pixel input field
PL_bpp_label = tk.Label(root, text="Payload bits per pixel:")
PL_bpp_label.grid(row=17, column=0)
PL_bpp_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
PL_bpp_entry.grid(row=17, column=1)
PL_bpp_unit = tk.Label(root, text="[-]")
PL_bpp_unit.grid(row=17, column=2)

# Payload duty cycle input field
PL_duty_cycle_label = tk.Label(root, text="Payload duty cycle:")
PL_duty_cycle_label.grid(row=18, column=0)
PL_duty_cycle_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
PL_duty_cycle_entry.grid(row=18, column=1)
PL_duty_cycle_unit = tk.Label(root, text="[%]")
PL_duty_cycle_unit.grid(row=18, column=2)

# Payload downlink time input field
PL_downlink_time_label = tk.Label(root, text="Payload downlink time:")
PL_downlink_time_label.grid(row=19, column=0)
PL_downlink_time_entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'), width=13)
PL_downlink_time_entry.grid(row=19, column=1)
PL_downlink_time_unit = tk.Label(root, text="[hr/day]")
PL_downlink_time_unit.grid(row=19, column=2)

# Modulation/Coding type input field
modulation_type_label = tk.Label(root, text="Modulation/Coding type:")
modulation_type_label.grid(row=20, column=0)
modulation_type_option_menu = ttk.Combobox(root, textvariable=selected_modulation_coding, values=modulation_coding_options, state="readonly", width=16)
modulation_type_option_menu.grid(row=20, column=1)

# Required BER input field
BER_req_label = tk.Label(root, text="Required BER (10^x):")
BER_req_label.grid(row=21, column=0)
BER_exponent_vals = [str(i) for i in range(-6, -5)]
BER_exponent_option_menu = ttk.Combobox(root, textvariable=BER_exponent, values=BER_exponent_vals, state="readonly", width=10)
BER_exponent_option_menu.grid(row=21, column=1)

# Output the calculated link margin
calculate_button = tk.Button(root, text="Calculate", command=calculate_link_margin)
calculate_button.grid(row=24, column=0)
link_margin_label_uplink=tk.Label(root, text="Link margin - Uplink")
link_margin_label_uplink.grid(row=22, column=0)
link_margin_output_uplink = tk.Label(root, text="", width=13)
link_margin_output_uplink.grid(row=22, column=1)
link_margin_output_uplink_units = tk.Label(root, text="[dB]")
link_margin_output_uplink_units.grid(row=22, column=2)
link_margin_label_downlink=tk.Label(root, text="Link margin - Downlink")
link_margin_label_downlink.grid(row=23, column=0)
link_margin_output_downlink = tk.Label(root, text="", width=13)
link_margin_output_downlink.grid(row=23, column=1)
link_margin_output_downlink_units = tk.Label(root, text="[dB]")
link_margin_output_downlink_units.grid(row=23, column=2)

# Citation generator
citation_generator_button = tk.Button(root, text="Copy BibTeX citation to clipboard", command=generate_bibtex(title, version))
citation_generator_button.grid(row=24, column=1)


root.mainloop()