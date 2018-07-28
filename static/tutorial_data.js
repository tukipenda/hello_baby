tutorial_messages=[
    "Welcome to the tutorial! The first step is to set up the warmer!",
    "Next you adjust the pressures",
]

popup_messages=[
     {
        'toggle_heat': {'text': "Click here to turn warmer on", 'position':'right'},
        'mask_size': {'text': "Select a mask", 'position':'bottom'}
     },
     {
        'prep_warmer': {'text': "Choose warmer settings", 'position':'right'},
        'PIP-div': {'text': 'Adjust the sliders to set pressures', 'position':'bottom'},
        'supplies': {'text': "When you are done setting pressures, you can pick supplies.", 'position':'right'}
     },
     {

     }
]

scenario_tutorial = {
    "scenario_text": "You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 32 weeks.",
    "PE": {
        "vitals": {
            "o2sat": 55,
            "o2sat_updated": 0,
            "hr": 120,
            "rr": 0,
            "sbp": 75,
            "dbp": 50,
            "temp": 35,
            "weight": 2.25
        },
        "resp": {
            "breath_sounds": "None",
            "chest_rise": "None",
            "wob": "None",
            "is_grunting": false,
            "is_spontaneous": false
        },
        "cardiac": {
            "murmur": "no murmur",
            "sounds": "normal S1/S2",
            "femoral_pulse": "2+",
            "brachial_pulse": "2+"
        },
        "secretions": {
            "quantity": "moderate",
            "below_cords": false,
            "color": "clear",
            "thickness": "thin"
        },
        "abd": {
            "bs": "+bs",
            "palpate": "soft, no HSM"
        },
        "neuro": {
            "loc": "no cry",
            "motor_activity": "not moving",
            "motor_deficit": "none"
        },
        "skin": {
            "color": "blue",
            "is_dry": false,
            "texture": "term infant skin"
        },
        "other": {
            "scalp": "no caput",
            "clavicles": "no clavicular fracture",
            "ears": "normally positioned",
            "eyes": "red reflex intact bilaterally",
            "umbilical_cord": "normal 3 vessel cord",
            "palate": "palate intact",
            "lips": "no cleft lips",
            "gu": "normal genitalia",
            "hips": "no hip click",
            "spine": "no dimple",
            "anus": "patent anus"
        }
    },
    "resusc": {
        "vent": {
            "efficacy": 0,
            "is_mouth_open": false,
            "positioning": 0,
            "is_airway_open": true,
            "has_air_leak": false,
            "set_rate": "0",
            "vent_type": "spontaneous"
        },
        "cpr": {
            "event_rate": 0,
            "btc_breaths": 0,
            "btc_compressions": 0,
            "cpr_depth": "0",
            "efficacy": 0
        },
        "uvc": {
            "is_uvc_placed": false,
            "medications_given": "[]"
        }
    },
    "mom": {
        "age": 25,
        "PNL": "Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative",
        "hsv": "No history of HSV and has no active lesions.",
        "gbs": "GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery.",
        "rom": "ROM occurred 16 hours ago.",
        "gp": "G1PO"
    },
    "baby": {
        "ga": "32",
        "neonatal_complications": "None",
        "is_delivered": null
    },
    "warmer": {
        "is_turned_on": false,
        "suction": 0,
        "fio2": 100,
        "flow": 0,
        "temp_mode": "manual",
        "peep": 0,
        "pip": 0,
        "pop": 0
    },
    "supplies": [{
        "size": null,
        "name": "pulse_ox",
        "is_available": false,
        "is_using": false,
        "pp": "pulse_ox"
    }, {
        "size": null,
        "name": "hat",
        "is_available": false,
        "is_using": false,
        "pp": "hat"
    }, {
        "size": null,
        "name": "transwarmer",
        "is_available": false,
        "is_using": false,
        "pp": "transwarmer"
    }, {
        "size": null,
        "name": "plastic_bag",
        "is_available": false,
        "is_using": false,
        "pp": "plastic_bag"
    }, {
        "size": null,
        "name": "temp_probe",
        "is_available": false,
        "is_using": false,
        "pp": "temp_probe"
    }, {
        "size": null,
        "name": "blankets",
        "is_available": false,
        "is_using": false,
        "pp": "blankets"
    }, {
        "size": null,
        "name": "bulb_suction",
        "is_available": false,
        "is_using": false,
        "pp": "bulb_suction"
    }, {
        "size": null,
        "name": "meconium_aspirator",
        "is_available": false,
        "is_using": false,
        "pp": "meconium_aspirator"
    }, {
        "size": null,
        "name": "stethoscope",
        "is_available": false,
        "is_using": false,
        "pp": "stethoscope"
    }, {
        "size": null,
        "name": "epinephrine",
        "is_available": false,
        "is_using": false,
        "pp": "epinephrine"
    }, {
        "size": null,
        "name": "normal_saline_bag",
        "is_available": false,
        "is_using": false,
        "pp": "normal_saline_bag"
    }, {
        "size": null,
        "name": "cord_clamp",
        "is_available": false,
        "is_using": false,
        "pp": "cord_clamp"
    }, {
        "size": null,
        "name": "scalpel",
        "is_available": false,
        "is_using": false,
        "pp": "scalpel"
    }, {
        "size": null,
        "name": "flush",
        "is_available": false,
        "is_using": false,
        "pp": "flush"
    }, {
        "size": null,
        "name": "UVC",
        "is_available": false,
        "is_using": false,
        "pp": "UVC"
    }, {
        "size": "0",
        "name": "laryngoscope",
        "is_available": false,
        "is_using": false,
        "pp": "laryngoscope: 0"
    }, {
        "size": "1",
        "name": "laryngoscope",
        "is_available": false,
        "is_using": false,
        "pp": "laryngoscope: 1"
    }, {
        "size": "00",
        "name": "laryngoscope",
        "is_available": false,
        "is_using": false,
        "pp": "laryngoscope: 00"
    }, {
        "size": "2.5",
        "name": "ett",
        "is_available": false,
        "is_using": false,
        "pp": "ett: 2.5"
    }, {
        "size": "3",
        "name": "ett",
        "is_available": false,
        "is_using": false,
        "pp": "ett: 3"
    }, {
        "size": "3.5",
        "name": "ett",
        "is_available": false,
        "is_using": false,
        "pp": "ett: 3.5"
    }, {
        "size": "Infant",
        "name": "mask",
        "is_available": true,
        "is_using": false,
        "pp": "mask: Infant"
    }, {
        "size": "Preemie",
        "name": "mask",
        "is_available": true,
        "is_using": false,
        "pp": "mask: Preemie"
    }],
    "tasks": [{
        "name": "fetch",
        "supply_name": "pulse_ox",
        "size": null,
        "pp": "fetch pulse_ox"
    }, {
        "name": "fetch",
        "supply_name": "hat",
        "size": null,
        "pp": "fetch hat"
    }, {
        "name": "fetch",
        "supply_name": "transwarmer",
        "size": null,
        "pp": "fetch transwarmer"
    }, {
        "name": "fetch",
        "supply_name": "plastic_bag",
        "size": null,
        "pp": "fetch plastic_bag"
    }, {
        "name": "fetch",
        "supply_name": "temp_probe",
        "size": null,
        "pp": "fetch temp_probe"
    }, {
        "name": "fetch",
        "supply_name": "blankets",
        "size": null,
        "pp": "fetch blankets"
    }, {
        "name": "fetch",
        "supply_name": "bulb_suction",
        "size": null,
        "pp": "fetch bulb_suction"
    }, {
        "name": "fetch",
        "supply_name": "meconium_aspirator",
        "size": null,
        "pp": "fetch meconium_aspirator"
    }, {
        "name": "fetch",
        "supply_name": "stethoscope",
        "size": null,
        "pp": "fetch stethoscope"
    }, {
        "name": "fetch",
        "supply_name": "epinephrine",
        "size": null,
        "pp": "fetch epinephrine"
    }, {
        "name": "fetch",
        "supply_name": "normal_saline_bag",
        "size": null,
        "pp": "fetch normal_saline_bag"
    }, {
        "name": "fetch",
        "supply_name": "cord_clamp",
        "size": null,
        "pp": "fetch cord_clamp"
    }, {
        "name": "fetch",
        "supply_name": "scalpel",
        "size": null,
        "pp": "fetch scalpel"
    }, {
        "name": "fetch",
        "supply_name": "flush",
        "size": null,
        "pp": "fetch flush"
    }, {
        "name": "fetch",
        "supply_name": "UVC",
        "size": null,
        "pp": "fetch UVC"
    }, {
        "name": "fetch",
        "supply_name": "laryngoscope",
        "size": "0",
        "pp": "fetch laryngoscope: 0"
    }, {
        "name": "fetch",
        "supply_name": "laryngoscope",
        "size": "1",
        "pp": "fetch laryngoscope: 1"
    }, {
        "name": "fetch",
        "supply_name": "laryngoscope",
        "size": "00",
        "pp": "fetch laryngoscope: 00"
    }, {
        "name": "fetch",
        "supply_name": "ett",
        "size": "2.5",
        "pp": "fetch ett: 2.5"
    }, {
        "name": "fetch",
        "supply_name": "ett",
        "size": "3",
        "pp": "fetch ett: 3"
    }, {
        "name": "fetch",
        "supply_name": "ett",
        "size": "3.5",
        "pp": "fetch ett: 3.5"
    }, {
        "name": "fetch",
        "supply_name": "mask",
        "size": "Infant",
        "pp": "fetch mask: Infant"
    }, {
        "name": "fetch",
        "supply_name": "mask",
        "size": "Preemie",
        "pp": "fetch mask: Preemie"
    }, {
        "name": "use",
        "supply_name": "pulse_ox",
        "size": null,
        "pp": "use pulse_ox"
    }, {
        "name": "use",
        "supply_name": "hat",
        "size": null,
        "pp": "use hat"
    }, {
        "name": "use",
        "supply_name": "transwarmer",
        "size": null,
        "pp": "use transwarmer"
    }, {
        "name": "use",
        "supply_name": "plastic_bag",
        "size": null,
        "pp": "use plastic_bag"
    }, {
        "name": "use",
        "supply_name": "temp_probe",
        "size": null,
        "pp": "use temp_probe"
    }, {
        "name": "use",
        "supply_name": "blankets",
        "size": null,
        "pp": "use blankets"
    }, {
        "name": "use",
        "supply_name": "bulb_suction",
        "size": null,
        "pp": "use bulb_suction"
    }, {
        "name": "use",
        "supply_name": "meconium_aspirator",
        "size": null,
        "pp": "use meconium_aspirator"
    }, {
        "name": "use",
        "supply_name": "stethoscope",
        "size": null,
        "pp": "use stethoscope"
    }, {
        "name": "use",
        "supply_name": "epinephrine",
        "size": null,
        "pp": "use epinephrine"
    }, {
        "name": "use",
        "supply_name": "normal_saline_bag",
        "size": null,
        "pp": "use normal_saline_bag"
    }, {
        "name": "use",
        "supply_name": "cord_clamp",
        "size": null,
        "pp": "use cord_clamp"
    }, {
        "name": "use",
        "supply_name": "scalpel",
        "size": null,
        "pp": "use scalpel"
    }, {
        "name": "use",
        "supply_name": "flush",
        "size": null,
        "pp": "use flush"
    }, {
        "name": "use",
        "supply_name": "UVC",
        "size": null,
        "pp": "use UVC"
    }, {
        "name": "use",
        "supply_name": "laryngoscope",
        "size": "0",
        "pp": "use laryngoscope: 0"
    }, {
        "name": "use",
        "supply_name": "laryngoscope",
        "size": "1",
        "pp": "use laryngoscope: 1"
    }, {
        "name": "use",
        "supply_name": "laryngoscope",
        "size": "00",
        "pp": "use laryngoscope: 00"
    }, {
        "name": "use",
        "supply_name": "ett",
        "size": "2.5",
        "pp": "use ett: 2.5"
    }, {
        "name": "use",
        "supply_name": "ett",
        "size": "3",
        "pp": "use ett: 3"
    }, {
        "name": "use",
        "supply_name": "ett",
        "size": "3.5",
        "pp": "use ett: 3.5"
    }, {
        "name": "use",
        "supply_name": "mask",
        "size": "Infant",
        "pp": "use mask: Infant"
    }, {
        "name": "use",
        "supply_name": "mask",
        "size": "Preemie",
        "pp": "use mask: Preemie"
    }, {
        "name": "dry",
        "pp": "dry"
    }, {
        "name": "stimulate",
        "pp": "stimulate"
    }, {
        "name": "bulb_suction",
        "pp": "bulb_suction"
    }, {
        "name": "deep_suction",
        "pp": "deep_suction"
    }],
    "PEtext": {
        "appearance": "32 week old infant.  Skin is blue and not dry. Term infant skin. Infant is not breathing. There is no chest rise. Mouth is closed. Infant is lying flat, no chin lift or jaw thrust.",
        "resp": "Infant is not breathing. There are no breath sounds. There is no chest rise. Secretions are moderate, thin, and clear. ",
        "cardiac": "Normal s1/s2. There is no murmur. Pulses are 2+ brachial and 2+ femoral. Heart rate is 120.",
        "abd": "Abdomen is soft, no HSM. +bs.",
        "neuro": "Infant is not crying. Infant is not moving.",
        "other": "Infant does not have a caput. No clavicular fracture. Ears are normally positioned. Red reflex intact bilaterally. Normal 3 vessel cord. Palate intact. No cleft lips. Normal genitalia. No hip click. No dimple. Patent anus"
    },
    "app_mode": "practice"
}