from .models import (
	Condition,
	ConditionQuestion,
	Insurance,
	PatientInfo,
	states,
	MedicalHistory, HealthRecord, PatientFamilyHistory, PatientIntake,
)


QUESTION_TYPE_TO_COMPONENT = {
	ConditionQuestion.TEXT: "text",
	ConditionQuestion.YES_NO: "radio",
	ConditionQuestion.NUMBER: "number",
	ConditionQuestion.DATE: "date",
	ConditionQuestion.SINGLE_CHOICE: "select",
	ConditionQuestion.MULTIPLE_CHOICE: "checkbox",
}


CONDITION_REQUEST_OPTIONS = [
	{"value": "YES", "label": "Yes"},
	{"value": "NO", "label": "No"},
]


def _build_options(choice_pairs):
	return [{"value": value, "label": label} for value, label in choice_pairs]


def _get_field_choice_options(model_class, field_name):
	field = model_class._meta.get_field(field_name)
	return _build_options(field.choices)


def _build_question_options(question):
	if not question.choice_set_id:
		return []

	return [
		{"value": choice.id, "label": choice.text}
		for choice in question.choice_set.choices.all()
	]


def generate_intake_form_json(include_condition_questions=True):
	"""
	Return a JSON-serializable schema for rendering the intake form on the frontend.

	The output is intentionally React-friendly and organized as sections/fields.
	Each field includes a stable key, type, required flag, and options when relevant.
	"""

	form_schema = {
		"formKey": "patient-intake",
		"version": 1,
		"sections": [
			{
				"id": "patient_info",
				"title": "Patient Information",
				"fields": [
					{
						"name": "first_name",
						"label": "First Name",
						"component": "text",
						"required": True,
					},
					{
						"name": "last_name",
						"label": "Last Name",
						"component": "text",
						"required": True,
					},
					{
						"name": "date_of_birth",
						"label": "Date of Birth",
						"component": "date",
						"required": True,
					},
					{
						"name": "email",
						"label": "Email",
						"component": "email",
						"required": True,
					},
					{
						"name": "phone_number",
						"label": "Phone Number",
						"component": "tel",
						"required": False,
					},
					{
						"name": "address",
						"label": "Address",
						"component": "textarea",
						"required": False,
					},
					{
						"name": "state",
						"label": "State",
						"component": "select",
						"required": False,
						"options": _build_options(states),
					},
				],
			},
			{
				"id": "patient_intake",
				"title": "Patient Intake",
				"fields": [
					{
						"name": "height",
						"label": "Height (inches)",
						"component": "number",
						"required": False,
					},
					{
						"name": "weight",
						"label": "Weight (lbs)",
						"component": "number",
						"required": False,
					},
				],
			},

						{
				"id": "patient_intake_vitals",
				"title": "Patient Intake Vitals",
				"fields": [
					{
						"name": "blood_pressure",
						"label": "Blood Pressure",
						"component": "text",
						"required": False,
					},
					{
						"name": "vital_signs",
						"label": "Vital Signs",
						"component": "textarea",
						"required": False,
					},
				],
			},



			{
				"id": "insurance",
				"title": "Insurance",
				"repeatable": False,
				"fields": [
					{
						"name": "insurance_type",
						"label": "Insurance Type",
						"component": "select",
						"required": True,
						"options": _build_options(Insurance.INSURANCE_TYPES),
					},
					{
						"name": "primary_insured",
						"label": "Primary Insured",
						"component": "checkbox",
						"required": False,
					},
					{
						"name": "insurance_carrier",
						"label": "Insurance Carrier",
						"component": "text",
						"required": False,
					},
					{
						"name": "carrier_phone",
						"label": "Carrier Phone",
						"component": "tel",
						"required": False,
					},
					{
						"name": "group_id",
						"label": "Group ID",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["RX"]},
					},
					{
						"name": "patient_id_rx",
						"label": "Patient ID (RX)",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["RX"]},
					},
					{
						"name": "bin",
						"label": "BIN",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["RX"]},
					},
					{
						"name": "pcn",
						"label": "PCN",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["RX"]},
					},
					{
						"name": "adjuster_name",
						"label": "Adjuster Name",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["PIP", "WC"]},
					},
					{
						"name": "adjuster_phone",
						"label": "Adjuster Phone",
						"component": "tel",
						"required": False,
						"showWhen": {"insurance_type": ["PIP", "WC"]},
					},
					{
						"name": "policy_number",
						"label": "Policy Number",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["PIP"]},
					},
					{
						"name": "claim_number",
						"label": "Claim Number",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["PIP", "WC"]},
					},
					{
						"name": "date_of_accident",
						"label": "Date of Accident",
						"component": "date",
						"required": False,
						"showWhen": {"insurance_type": ["PIP"]},
					},
					{
						"name": "payer_name",
						"label": "Payer Name",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["WC"]},
					},
					{
						"name": "date_of_injury",
						"label": "Date of Injury",
						"component": "date",
						"required": False,
						"showWhen": {"insurance_type": ["WC"]},
					},
					{
						"name": "employer_name",
						"label": "Employer Name",
						"component": "text",
						"required": False,
						"showWhen": {"insurance_type": ["WC"]},
					},
				],
			},
			{
				"id": "medical_history",
				"title": "Medical History",
				"repeatable": True,
				"fields": [
					{
						"name": "condition",
						"label": "Condition",
						"component": "text",
						"required": True,
					},
					{
						"name": "diagnosis_date",
						"label": "Diagnosis Date",
						"component": "date",
						"required": False,
					},
					{
						"name": "notes",
						"label": "Notes",
						"component": "textarea",
						"required": False,
					},
				],
			},
			{
				"id": "HealthRecords",
				"title": "Health Records",
				"repeatable": True,
				"fields": [
					{
						"name": "record_type",
						"label": "Record Type",
						"component": "select",
						"required": True,
						"options": _get_field_choice_options(HealthRecord, "record_type"),
					},
					{
						"name": "record_date",
						"label": "Record Date",
						"component": "date",
						"required": False,
					},
					{
						"name": "description",
						"label": "Description",
						"component": "textarea",
						"required": False,
					},
				],
			},
			{
				"id": "family_history",
				"title": "Family History",
				"fields": [
					{
						"name": "asthama",
						"label": "Asthama",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "asthama"),
					},
					{
						"name": "bleeding_tendency",
						"label": "Bleeding Tendency",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "bleeding_tendency"),
					},
					{
						"name": "cancer",
						"label": "Cancer",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "cancer"),
					},
					{
						"name": "colitis",
						"label": "Colitis",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "colitis"),
					},
					{
						"name": "depression",
						"label": "Depression",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "depression"),
					},
					{
						"name": "diabetes",
						"label": "Diabetes",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "diabetes"),
					},
					{
						"name": "epilepsy",
						"label": "Epilepsy",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "epilepsy"),
					},
					{
						"name": "heart_attack",
						"label": "Heart Attack",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "heart_attack"),
					},
					{
						"name": "high_blood_pressure",
						"label": "High Blood Pressure",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "high_blood_pressure"),
					},
					{
						"name": "kidney_disease",
						"label": "Kidney Disease",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "kidney_disease"),
					},
					{
						"name": "leukemia",
						"label": "Leukemia",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "leukemia"),
					},
					{
						"name": "migraine",
						"label": "Migraine",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "migraine"),
					},
					{
						"name": "schizophrenia",
						"label": "Schizophrenia",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "schizophrenia"),
					},
					{
						"name": "stomach_ulcers",
						"label": "Stomach Ulcers",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "stomach_ulcers"),
					},
					{
						"name": "stroke",
						"label": "Stroke",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "stroke"),
					},
					{
						"name": "suicide",
						"label": "Suicide",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "suicide"),
					},
					{
						"name": "tuberculosis",
						"label": "Tuberculosis",
						"component": "radio",
						"required": False,
						"options": _get_field_choice_options(PatientFamilyHistory, "tuberculosis"),
					},
				],
			},
		],
	}

	
	if not include_condition_questions:
		return form_schema

	condition_request_fields = []
	condition_sections = []
	conditions = Condition.objects.prefetch_related("questions__choice_set__choices").all()
	for condition in conditions:
		requested_field_name = f"condition_requests.condition_{condition.id}_requested"
		condition_request_fields.append(
			{
				"name": f"condition_{condition.id}_requested",
				"conditionId": condition.id,
				"conditionCode": condition.code,
				"label": f"Request {condition.name}?",
				"component": "radio",
				"required": False,
				"options": CONDITION_REQUEST_OPTIONS,
			}
		)

		questions = (
			condition.questions.select_related("choice_set")
			.all()
			.order_by("order")
		)

		fields = []
		for question in questions:
			field = {
				"name": f"condition_{condition.id}_question_{question.id}",
				"questionId": question.id,
				"label": question.question,
				"component": QUESTION_TYPE_TO_COMPONENT.get(question.question_type, "text"),
				"questionType": question.question_type,
				"required": question.required,
				"showWhen": {requested_field_name: ["YES"]},
			}

			options = _build_question_options(question)
			if options:
				field["options"] = options

			fields.append(field)

		condition_sections.append(
			{
				"id": f"condition_{condition.code}",
				"conditionId": condition.id,
				"conditionCode": condition.code,
				"title": condition.name,
				"showWhen": {requested_field_name: ["YES"]},
				"fields": fields,
			}
		)

	form_schema["sections"].append(
		{
			"id": "condition_requests",
			"title": "Condition Requests",
			"fields": condition_request_fields,
		}
	)

	form_schema["sections"].append(
		{
			"id": "conditions",
			"title": "Condition-Specific Questions",
			"groups": condition_sections,
		}
	)

	return form_schema





