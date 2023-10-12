import math as m

### CONSTANTS ###
v_light = 3 * 10**8

def val_to_dB(num):
    '''Simple function to translate values to dB'''
    return 10 * m.log10(num)

def EIRP_calc(P_transmitter, Loss, Gain):
    '''Obtain the EIRP [dB] of the transmitter'''
    # Conversion to dB
    P_TX = P_transmitter
    L_TX = Loss
    G_TX = Gain

    # EIRP [dB] calculated
    EIRP = P_TX + L_TX + G_TX

    return EIRP

def transmitter_pointing_loss(freq_GHz, diam, pointing_offset):
    '''Obtain the pointing loss of the transmitter'''
    # Half power angle calculated
    a_half = 21 / (float(freq_GHz) * float(diam))
    # Antenna loss [dB] calculated
    L_pointing = 12 * (float(pointing_offset) / a_half)**2

    return L_pointing

def transmitter_gain(freq_down_GHz, transmitter_diam, antenna_efficiency=0.55):
    '''Obtain G_TX [dB] of the transmitter (efficiency assumed 0.55 if unchanged)'''
    # Calculate wavelength of EM radiation
    wavelength = v_light / (float(freq_down_GHz) * 10**9)
    # Antenna gain [-] calculated
    gain = float(antenna_efficiency) * ((m.pi * float(transmitter_diam)) / wavelength)**2
    # Antenna gain [dB] calculated
    G_antenna = val_to_dB(gain)

    return G_antenna

def space_loss(freq_down_GHz, d_earth_sun, d_sc_sun, elong_angle):
    '''Obtain the space loss for deep space missions'''
    # Calculate S (S/C to GS distance)
    S = m.sqrt(d_earth_sun**2 + d_sc_sun**2 - (2 * d_earth_sun * d_sc_sun * m.cos(m.radians(float(elong_angle)))))
    # Calculate wavelength
    wavelength = v_light / (float(freq_down_GHz) * 10**9)
    # Calculate space loss [-]
    loss = (wavelength / (4 * m.pi * S))**2
    # Calculate space loss [dB]
    L_s = val_to_dB(loss)

    return L_s

def required_data_rate(bits_per_pixel, swath_width, pixel_size, sc_alt, mu, planetary_r):
    '''Obtain downlink required data rate'''
    # S/C velocity relative to ground calculated
    V_ground = m.sqrt(mu / (sc_alt + planetary_r)) * (planetary_r / (planetary_r + sc_alt))