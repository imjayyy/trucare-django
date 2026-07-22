from .models import (
	Condition,
	ConditionQuestion,
	Insurance,
	states,
)


QUESTION_TYPE_TO_COMPONENT = {
	ConditionQuestion.TEXT: "text",
	ConditionQuestion.YES_NO: "radio",
	ConditionQuestion.NUMBER: "number",
	ConditionQuestion.DATE: "date",
	ConditionQuestion.SINGLE_CHOICE: "select",
	ConditionQuestion.MULTIPLE_CHOICE: "multiselect",
}


def _build_options(choice_pairs):
	return [{"value": value, "label": label} for value, label in choice_pairs]


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
				"id": "insurance",
				"title": "Insurance",
				"repeatable": True,
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
		],
	}

	if not include_condition_questions:
		return form_schema

	condition_sections = []
	conditions = Condition.objects.prefetch_related("questions__choice_set__choices").all()
	for condition in conditions:
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
				"fields": fields,
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





