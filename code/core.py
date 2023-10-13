import math as m
import pyperclip as pclip

### CONSTANTS ###
v_light = 3 * 10**8
boltzmann_const = 1.38 * 10**(-23)

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

### GAIN/LOSS FUNCTIONS ###
def val_to_dB(num):
    '''Simple function to translate values to dB'''
    return 10 * m.log10(num)

def EIRP_calc(P_transmitter, Loss_dB, Gain_dB):
    '''Obtain the EIRP [dB] of the transmitter'''
    # Conversion to dB
    P_TX = val_to_dB(P_transmitter)
    L_TX = Loss_dB
    G_TX = Gain_dB

    # EIRP [dB] calculated
    EIRP = P_TX + L_TX + G_TX

    return EIRP

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
    S = m.sqrt(d_earth_sun**2 + d_sc_sun**2 - (2 * d_earth_sun * d_sc_sun * m.cos(m.radians(float(elong_angle)))))
    # Calculate lambda (wavelength)
    wavelength = v_light / (float(freq_transmitter_GHz) * 10**9)
    # Calculate space loss [-]
    loss = (wavelength / (4 * m.pi * S))**2
    # Calculate space loss [dB]
    L_s = val_to_dB(loss)
    
    return L_s

def space_loss(freq_transmitter_GHz, altitude):
    '''Obtain the space loss for near-Earth missions (inlcuding Moon)'''
    # Calculate S (S/C to GS distance)
    S = float(altitude)
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
    V_ground = m.sqrt(float(mu) / (float(sc_alt) + float(planetary_r))) * (float(planetary_r) / (float(planetary_r) + float(sc_alt)))
    # Pixel size calculated
    p_size = float(sc_alt) * 1000 * m.tan(m.radians(float(pixel_size)))
    # Swath width calculated
    sw_width = float(sc_alt) * 1000 * m.tan(m.radians(float(swath_width)))
    # Generated data rate calculated
    R_G = float(bits_per_pixel) * ((sw_width * V_ground) / (p_size**2))
    # Payload-required data rate calculated
    R_req = R_G * (float(PL_duty_cycle)/100) / (float(PL_downlink_time)/24)
    # Transmitted data rate (due to channel coding) calculated
    R_transmitted = R_req / float(code_rate)
    # Transmitted data rate [dB]
    R_dB = val_to_dB(R_transmitted)
    
    return R_dB
    