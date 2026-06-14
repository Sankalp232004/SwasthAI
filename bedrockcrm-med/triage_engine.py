"""
SwasthAI Triage Engine
CRITICAL: This is a PURE FUNCTION.

Rules:
- No DB access
- No side effects
- No mutation
- Input → Output only

Logic:
- Use if / elif (no loops for priority)
- No scores or totals
- Red flags short-circuit immediately
- Highest severity rule wins
"""

from dataclasses import dataclass
from typing import List, Dict, Any


# Triage Engine Version
ENGINE_VERSION = "1.0.0"


@dataclass(frozen=True)
class TriageInput:
    """
    Exactly 15 inputs - Fixed schema - All required.
    Invalid input → reject request.
    """
    # Vital Signs (5 inputs)
    heart_rate: int              # bpm
    systolic_bp: int             # mmHg
    diastolic_bp: int            # mmHg
    respiratory_rate: int        # breaths per minute
    temperature: float           # Celsius
    
    # Consciousness & Pain (3 inputs)
    consciousness_level: str     # ALERT, VERBAL, PAIN, UNRESPONSIVE (AVPU)
    pain_level: int              # 0-10 scale
    pain_location: str           # body location
    
    # Symptoms (4 inputs)
    chest_pain: bool
    difficulty_breathing: bool
    bleeding_severity: str       # NONE, MINOR, MODERATE, SEVERE, LIFE_THREATENING
    symptom_duration_hours: int
    
    # Risk Factors (3 inputs)
    is_pregnant: bool
    has_diabetes: bool
    has_heart_condition: bool


@dataclass(frozen=True)
class TriageOutput:
    """
    Output format with priority and explicit reasons.
    """
    priority: str
    reasons: List[str]
    red_flags: List[str]
    engine_version: str


def validate_triage_input(data: Dict[str, Any]) -> tuple[bool, str, TriageInput | None]:
    """
    Validate all 15 inputs explicitly.
    Returns: (is_valid, error_message, validated_input)
    Invalid input → reject request.
    """
    
    required_fields = [
        'heart_rate', 'systolic_bp', 'diastolic_bp', 'respiratory_rate', 'temperature',
        'consciousness_level', 'pain_level', 'pain_location',
        'chest_pain', 'difficulty_breathing', 'bleeding_severity', 'symptom_duration_hours',
        'is_pregnant', 'has_diabetes', 'has_heart_condition'
    ]
    
    # Check all fields present
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}", None
    
    # Validate heart_rate (40-220 bpm valid range)
    if not isinstance(data['heart_rate'], int):
        return False, "heart_rate must be an integer", None
    if data['heart_rate'] < 20 or data['heart_rate'] > 300:
        return False, "heart_rate must be between 20-300 bpm", None
    
    # Validate systolic_bp (50-300 mmHg valid range)
    if not isinstance(data['systolic_bp'], int):
        return False, "systolic_bp must be an integer", None
    if data['systolic_bp'] < 40 or data['systolic_bp'] > 300:
        return False, "systolic_bp must be between 40-300 mmHg", None
    
    # Validate diastolic_bp (30-200 mmHg valid range)
    if not isinstance(data['diastolic_bp'], int):
        return False, "diastolic_bp must be an integer", None
    if data['diastolic_bp'] < 20 or data['diastolic_bp'] > 200:
        return False, "diastolic_bp must be between 20-200 mmHg", None
    
    # Validate respiratory_rate (4-60 breaths/min valid range)
    if not isinstance(data['respiratory_rate'], int):
        return False, "respiratory_rate must be an integer", None
    if data['respiratory_rate'] < 4 or data['respiratory_rate'] > 60:
        return False, "respiratory_rate must be between 4-60 breaths/min", None
    
    # Validate temperature (30-45°C valid range)
    if not isinstance(data['temperature'], (int, float)):
        return False, "temperature must be a number", None
    if data['temperature'] < 30 or data['temperature'] > 45:
        return False, "temperature must be between 30-45°C", None
    
    # Validate consciousness_level
    valid_consciousness = ['ALERT', 'VERBAL', 'PAIN', 'UNRESPONSIVE']
    if data['consciousness_level'] not in valid_consciousness:
        return False, f"consciousness_level must be one of: {valid_consciousness}", None
    
    # Validate pain_level (0-10)
    if not isinstance(data['pain_level'], int):
        return False, "pain_level must be an integer", None
    if data['pain_level'] < 0 or data['pain_level'] > 10:
        return False, "pain_level must be between 0-10", None
    
    # Validate pain_location (non-empty string)
    if not isinstance(data['pain_location'], str) or len(data['pain_location'].strip()) == 0:
        return False, "pain_location must be a non-empty string", None
    
    # Validate chest_pain (boolean)
    if not isinstance(data['chest_pain'], bool):
        return False, "chest_pain must be a boolean", None
    
    # Validate difficulty_breathing (boolean)
    if not isinstance(data['difficulty_breathing'], bool):
        return False, "difficulty_breathing must be a boolean", None
    
    # Validate bleeding_severity
    valid_bleeding = ['NONE', 'MINOR', 'MODERATE', 'SEVERE', 'LIFE_THREATENING']
    if data['bleeding_severity'] not in valid_bleeding:
        return False, f"bleeding_severity must be one of: {valid_bleeding}", None
    
    # Validate symptom_duration_hours (0+)
    if not isinstance(data['symptom_duration_hours'], int):
        return False, "symptom_duration_hours must be an integer", None
    if data['symptom_duration_hours'] < 0:
        return False, "symptom_duration_hours must be non-negative", None
    
    # Validate boolean risk factors
    if not isinstance(data['is_pregnant'], bool):
        return False, "is_pregnant must be a boolean", None
    if not isinstance(data['has_diabetes'], bool):
        return False, "has_diabetes must be a boolean", None
    if not isinstance(data['has_heart_condition'], bool):
        return False, "has_heart_condition must be a boolean", None
    
    # All validations passed - create immutable input
    validated = TriageInput(
        heart_rate=data['heart_rate'],
        systolic_bp=data['systolic_bp'],
        diastolic_bp=data['diastolic_bp'],
        respiratory_rate=data['respiratory_rate'],
        temperature=float(data['temperature']),
        consciousness_level=data['consciousness_level'],
        pain_level=data['pain_level'],
        pain_location=data['pain_location'].strip(),
        chest_pain=data['chest_pain'],
        difficulty_breathing=data['difficulty_breathing'],
        bleeding_severity=data['bleeding_severity'],
        symptom_duration_hours=data['symptom_duration_hours'],
        is_pregnant=data['is_pregnant'],
        has_diabetes=data['has_diabetes'],
        has_heart_condition=data['has_heart_condition']
    )
    
    return True, "", validated


def compute_triage(triage_input: TriageInput) -> TriageOutput:
    """
    PURE FUNCTION: Deterministic triage computation.
    
    Rules:
    - No DB access
    - No side effects
    - No mutation
    - Input → Output only
    - Red flags short-circuit immediately
    - Highest severity rule wins
    
    Priority order: EMERGENCY > RED > AMBER > GREEN
    """
    
    reasons: List[str] = []
    red_flags: List[str] = []
    
    # =========================================================================
    # EMERGENCY CHECKS - Immediate short-circuit
    # =========================================================================
    
    # E1: Unresponsive patient
    if triage_input.consciousness_level == 'UNRESPONSIVE':
        red_flags.append("Patient is unresponsive")
        reasons.append("AVPU scale: Unresponsive - requires immediate intervention")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E2: Life-threatening bleeding
    if triage_input.bleeding_severity == 'LIFE_THREATENING':
        red_flags.append("Life-threatening bleeding")
        reasons.append("Active life-threatening hemorrhage requires immediate intervention")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E3: Severe hypotension (systolic < 70)
    if triage_input.systolic_bp < 70:
        red_flags.append("Severe hypotension")
        reasons.append(f"Systolic BP critically low at {triage_input.systolic_bp} mmHg")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E4: Respiratory failure (rate < 8 or > 35)
    if triage_input.respiratory_rate < 8:
        red_flags.append("Respiratory depression")
        reasons.append(f"Respiratory rate dangerously low at {triage_input.respiratory_rate}/min")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    if triage_input.respiratory_rate > 35:
        red_flags.append("Severe respiratory distress")
        reasons.append(f"Respiratory rate critically elevated at {triage_input.respiratory_rate}/min")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E5: Extreme bradycardia (< 40 bpm)
    if triage_input.heart_rate < 40:
        red_flags.append("Severe bradycardia")
        reasons.append(f"Heart rate critically low at {triage_input.heart_rate} bpm")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E6: Extreme tachycardia (> 180 bpm)
    if triage_input.heart_rate > 180:
        red_flags.append("Severe tachycardia")
        reasons.append(f"Heart rate critically elevated at {triage_input.heart_rate} bpm")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E7: Severe hypothermia (< 32°C)
    if triage_input.temperature < 32:
        red_flags.append("Severe hypothermia")
        reasons.append(f"Body temperature critically low at {triage_input.temperature}°C")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # E8: Severe hyperthermia (> 41°C)
    if triage_input.temperature > 41:
        red_flags.append("Severe hyperthermia")
        reasons.append(f"Body temperature critically elevated at {triage_input.temperature}°C")
        return TriageOutput(
            priority="EMERGENCY",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # =========================================================================
    # RED CHECKS - Urgent, high priority
    # =========================================================================
    
    # R1: Responds only to pain
    if triage_input.consciousness_level == 'PAIN':
        red_flags.append("Altered consciousness - responds only to pain")
        reasons.append("AVPU scale: Pain response only - requires urgent evaluation")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R2: Chest pain with cardiac history
    if triage_input.chest_pain and triage_input.has_heart_condition:
        red_flags.append("Chest pain with cardiac history")
        reasons.append("Chest pain in patient with known heart condition requires urgent cardiac workup")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R3: Chest pain with difficulty breathing
    if triage_input.chest_pain and triage_input.difficulty_breathing:
        red_flags.append("Chest pain with respiratory distress")
        reasons.append("Combined chest pain and breathing difficulty suggests acute cardiopulmonary event")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R4: Severe bleeding
    if triage_input.bleeding_severity == 'SEVERE':
        red_flags.append("Severe bleeding")
        reasons.append("Active severe hemorrhage requires urgent intervention")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R5: Severe pain (9-10)
    if triage_input.pain_level >= 9:
        red_flags.append("Severe pain")
        reasons.append(f"Severe pain level ({triage_input.pain_level}/10) requires urgent assessment")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R6: Hypotension (systolic 70-90)
    if triage_input.systolic_bp < 90:
        red_flags.append("Hypotension")
        reasons.append(f"Low systolic BP at {triage_input.systolic_bp} mmHg requires urgent evaluation")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R7: Severe hypertension (systolic > 200 or diastolic > 120)
    if triage_input.systolic_bp > 200 or triage_input.diastolic_bp > 120:
        red_flags.append("Hypertensive urgency")
        reasons.append(f"Severely elevated BP ({triage_input.systolic_bp}/{triage_input.diastolic_bp}) requires urgent management")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R8: Pregnant with concerning symptoms
    if triage_input.is_pregnant and (triage_input.chest_pain or triage_input.difficulty_breathing or triage_input.bleeding_severity in ['MODERATE', 'SEVERE']):
        red_flags.append("Pregnancy with concerning symptoms")
        reasons.append("Pregnant patient with acute symptoms requires urgent OB evaluation")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R9: High fever (> 39.5°C)
    if triage_input.temperature > 39.5:
        red_flags.append("High fever")
        reasons.append(f"High fever at {triage_input.temperature}°C requires urgent evaluation")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # R10: Tachycardia with symptoms (> 130 bpm with chest pain or breathing difficulty)
    if triage_input.heart_rate > 130 and (triage_input.chest_pain or triage_input.difficulty_breathing):
        red_flags.append("Tachycardia with cardiopulmonary symptoms")
        reasons.append(f"Elevated heart rate ({triage_input.heart_rate} bpm) with symptoms requires urgent assessment")
        return TriageOutput(
            priority="RED",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # =========================================================================
    # AMBER CHECKS - Semi-urgent
    # =========================================================================
    
    # A1: Responds only to verbal stimuli
    if triage_input.consciousness_level == 'VERBAL':
        reasons.append("AVPU scale: Verbal response - requires timely evaluation")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A2: Moderate pain (6-8)
    if triage_input.pain_level >= 6:
        reasons.append(f"Moderate pain level ({triage_input.pain_level}/10) requires assessment")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A3: Chest pain without high-risk factors
    if triage_input.chest_pain:
        reasons.append("Chest pain present - requires evaluation")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A4: Difficulty breathing without other red flags
    if triage_input.difficulty_breathing:
        reasons.append("Breathing difficulty reported - requires assessment")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A5: Moderate bleeding
    if triage_input.bleeding_severity == 'MODERATE':
        reasons.append("Moderate bleeding - requires wound assessment")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A6: Fever (38-39.5°C)
    if triage_input.temperature >= 38:
        reasons.append(f"Fever at {triage_input.temperature}°C - requires evaluation")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A7: Elevated BP (systolic 160-200 or diastolic 100-120)
    if triage_input.systolic_bp >= 160 or triage_input.diastolic_bp >= 100:
        reasons.append(f"Elevated BP ({triage_input.systolic_bp}/{triage_input.diastolic_bp}) - monitoring needed")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A8: Tachycardia (100-130 bpm)
    if triage_input.heart_rate > 100:
        reasons.append(f"Elevated heart rate ({triage_input.heart_rate} bpm) - requires assessment")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A9: Diabetic with acute symptoms
    if triage_input.has_diabetes and triage_input.symptom_duration_hours < 6:
        reasons.append("Diabetic patient with acute symptoms - requires timely evaluation")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A10: Pregnant (routine flag for priority)
    if triage_input.is_pregnant:
        reasons.append("Pregnant patient - prioritized for timely care")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # A11: Prolonged symptoms > 48 hours
    if triage_input.symptom_duration_hours > 48:
        reasons.append(f"Symptoms persisting for {triage_input.symptom_duration_hours} hours - requires evaluation")
        return TriageOutput(
            priority="AMBER",
            reasons=reasons,
            red_flags=red_flags,
            engine_version=ENGINE_VERSION
        )
    
    # =========================================================================
    # GREEN - Standard priority
    # =========================================================================
    
    reasons.append("Vital signs stable, no red flags identified")
    return TriageOutput(
        priority="GREEN",
        reasons=reasons,
        red_flags=red_flags,
        engine_version=ENGINE_VERSION
    )


def triage_to_dict(output: TriageOutput) -> Dict[str, Any]:
    """Convert TriageOutput to dictionary for JSON response."""
    return {
        'priority': output.priority,
        'reasons': output.reasons,
        'red_flags': output.red_flags,
        'engine_version': output.engine_version
    }
