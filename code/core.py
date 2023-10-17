import math as m
import csv
import sys
import os
from tkinter import filedialog
import pyperclip as pclip

### CONSTANTS ###
v_light = 3 * 10**8
boltzmann_const = 1.38 * 10**(-23)
# Data format: gravitational parameter [km^3/s^2], mean radius [km], for Moon distance to Earth but distance to Sun otherwise [km]
celestial_body_data = {"Mercury": [22032, 2439.7, (58.366*10**6)],
                       "Venus": [324860, 6051.8, (108.01*10**6)],
                       "Earth":[398600, 6371.0, (149.28*10**6)],
                       "Moon": [4900, 1737.4, (0.3844*10**6)],
                       "Mars": [42828, 3389.5, (237.97*10**6)],
                       "Jupiter": [126687000, 69911, (778*10**6)],
                       "Saturn": [37931000, 58232, (1.4586*10**9)],
                       "Uranus": [5794000, 25362, (2.871*10**9)],
                       "Neptune": [6835100, 24622, (4.4727*10**9)]}

# Data format: rate [-], (E_b/N_o)_req [dB]
channel_coding_data = {"Uncoded": [1, 10.5],
                       "Reed-Solomon (only)": [1, 6.4],
                       "Convolutional: r=1/2": [1/2, 4.8],
                       "Convolutional-RS: r=1/2": [1/2, 2.5],
                       "Convolutional-RS: r=1/6": [1/6, 1.5],
                       "Turbo-Codes: r=1/2": [1/2, 1.0],
                       "Turbo-Codes: r=1/6": [1/6, 0.5],
                       "LDPC: r=3/4": [3/4, 0.5]}

### GUI UTILITY FUNCTIONS ###
def generate_bibtex(title, version):
    '''Generate a BibTeX entry straight to clipboard'''
    citation_content = f"""
    @software{{link_margin_calculator,
    author       = {{Adam Moëc}},
    title        = {{ {title} }},
    version      = {{ {version} }}, 
    year         = {{2023}},
    publisher    = {{TU Delft}},
    url          = {{https://github.com/Caasimov/SatComLinkBudget}},
    note         = {{Available under GPL-3.0 license}},
    }}"""
    pclip.copy(citation_content)
    
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def write_to_csv(uplink_data, downlink_data):
    '''Write loss/gain data to csv file'''
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    # Ask user for file path, and check if they cancelled the dialog
    if not file_path:
        return
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        headers = ["", "UPLINK LINK BUDGET", "", "", "DOWNLINK LINK BUDGET", ""]
        writer.writerow(headers)
        writer.writerow(["Quantity", "", "Value [dB]", "Quantity", "", "Value [dB]"])
        
        # Write data rows
        for (uplink_key, downlink_key) in zip(uplink_data.keys(), downlink_data.keys()):
            uplink_desc, uplink_val = uplink_data[uplink_key]
            downlink_desc, downlink_val = downlink_data[downlink_key]
            row = [uplink_key, uplink_desc, uplink_val, downlink_key, downlink_desc, downlink_val]
            writer.writerow(row)

### GAIN/LOSS FUNCTIONS ###
def val_to_dB(num):
    '''Simple function to translate values to dB'''
    dB = 10 * m.log10(num)
    return dB

def uplink_freq_GHz(freq_dlink_GHz, TAR):
    '''Obtain uplink frequency [GHz] from downlink frequency and turn around ratio (TAR)'''
    try:
        freq_ulink_GHz = float(freq_dlink_GHz) * float(TAR)
    except:
        return ""
    
    return freq_ulink_GHz

def pointing_loss(freq_GHz, diam, pointing_offset):
    '''Obtain the pointing loss of the transmitter/receiver'''
    # Half power angle calculated
    a_half = 21 / (float(freq_GHz) * float(diam))
    # Antenna loss [dB] calculated
    L_pointing = 12 * (float(pointing_offset) / a_half)**2

    return L_pointing

def transmitter_gain(freq_transmitter_GHz, transmitter_diam, antenna_efficiency):
    '''Obtain G_TX [dB] of the transmitter'''
    # Calculate wavelength of EM radiation
    wavelength = v_light / (float(freq_transmitter_GHz) * 10**9)
    # Antenna gain [-] calculated
    gain = float(antenna_efficiency) * ((m.pi * float(transmitter_diam)) / wavelength)**2
    # Antenna gain [dB] calculated
    G_antenna = val_to_dB(gain)

    return G_antenna

def space_loss_DS(freq_transmitter_GHz, d_earth_sun, d_sc_sun, elong_angle):
    '''Obtain the space loss for deep space missions'''
    # Calculate S (S/C to GS distance)
    S = 1000 * m.sqrt((d_earth_sun)**2 + (d_sc_sun)**2 - (2 * (d_earth_sun) * (d_sc_sun) * m.cos(m.radians(float(elong_angle)))))
    # Calculate lambda (wavelength)
    wavelength = v_light / (float(freq_transmitter_GHz) * 10**9)
    # Calculate space loss [-]
    loss = (wavelength / (4 * m.pi * S))**2
    # Calculate space loss [dB]
    L_s = val_to_dB(loss)
    
    return L_s

def space_loss(freq_transmitter_GHz, altitude, body_radius):
    '''Obtain the space loss for near-Earth missions (inlcuding Moon)'''
    # Calculate S (S/C to GS distance)
    S = m.sqrt((float(altitude) + body_radius)**2 - body_radius**2) * 1000
    # Calculate lambda (wavelength)
    wavelength = v_light / (float(freq_transmitter_GHz) * 10**9)
    # Calculate space loss [-]
    loss = (wavelength / (4 * m.pi * S))**2
    # Calculate space loss [dB]
    L_s = val_to_dB(loss)
    
    return L_s

def required_data_rate(bits_per_pixel, swath_width, pixel_size, sc_alt, PL_duty_cycle, PL_downlink_time, code_rate, mu, planetary_r):
    '''Obtain downlink required data rate'''
    # S/C velocity relative to ground calculated
    V_ground = m.sqrt(float(mu) / (float(sc_alt) + float(planetary_r))) * (float(planetary_r) / (float(planetary_r) + float(sc_alt))) * 1000
    # Pixel size calculated
    p_size = 2 * float(sc_alt) * 1000 * m.tan(m.radians(float(pixel_size)/(60*2)))
    # Swath width calculated
    sw_width = 2 * float(sc_alt) * 1000 * m.tan(m.radians(float(swath_width)/2))
    # Generated data rate calculated
    R_G = float(bits_per_pixel) * ((sw_width * V_ground) / (p_size**2))
    # Payload-required data rate calculated
    R_req = R_G * (float(PL_duty_cycle)/100) / (float(PL_downlink_time)/24)
    # Transmitted data rate (due to channel coding) calculated
    R_transmitted = R_req / float(code_rate)
    # Transmitted data rate [dB]
    R_dB = val_to_dB(R_transmitted)
    
    return R_dB

def sys_temp(freq_GHz, uplink=True):
    '''Obtain signal noise temperature (rough approximation from literature)'''
    # If no value for frequency has been given yet, then do not display a temp
    try:
        freq_GHz = float(freq_GHz)
    except:
        return ""
    
    if uplink:
        if 0.2 <= freq_GHz <= 20:
            return 614
        elif freq_GHz < 0.2:
            return ""
        else:
            return 763
    else:
        if freq_GHz < 0.2:
            return ""
        elif 0.2 < freq_GHz <= 2:
            return 221
        elif 2 < freq_GHz <=20:
            return 135
        else:
            return 424