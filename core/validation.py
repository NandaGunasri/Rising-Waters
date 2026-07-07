from core.config import LIMITS

def validate_inputs(form_data):
    """
    Validate and clean form data for flood prediction.
    
    Args:
        form_data (dict): Dictionary of inputs from request.form
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None, cleaned_data: dict or None)
    """
    cleaned_data = {}
    missing_fields = []
    invalid_format_fields = []
    out_of_bound_fields = []
    
    for key, rule in LIMITS.items():
        val = form_data.get(key, "").strip()
        
        if not val:
            missing_fields.append(rule["label"])
            continue
            
        try:
            float_val = float(val)
        except ValueError:
            invalid_format_fields.append(rule["label"])
            continue
            
        if float_val < rule["min"] or float_val > rule["max"]:
            out_of_bound_fields.append(
                f"{rule['label']} must be between {rule['min']} and {rule['max']}"
            )
            continue
            
        cleaned_data[key] = float_val
        
    # Check for compile errors
    if missing_fields:
        return (
            False,
            f"Please fill in all fields: {', '.join(missing_fields)}.",
            None
        )
        
    if invalid_format_fields:
        return (
            False,
            f"Please enter valid numeric values for: {', '.join(invalid_format_fields)}.",
            None
        )
        
    if out_of_bound_fields:
        return (
            False,
            f"Out-of-range values detected: {'; '.join(out_of_bound_fields)}.",
            None
        )
        
    return True, None, cleaned_data
