def prompt_user_for_yes_or_no(question, default="yes"):
    """
    Prompts the user for the answer to a yes or no question.

    :param question: The question to display to the user.
    :param default: The default answer. Defaults to "yes".

    :returns: True if the user chose yes, else returns False.

    :throws: ValueError if an invalid default answer is provided.
    :throws: ValueError if a mapping for a default answer could not be found.
    """
    # Answers to treat as valid options
    valid = {"yes": True, "y": True, "no": False, "n": False}

    # Build the prompt for the question, taking into account the default option
    if default is None:
        prompt = "[y/n]"
    elif default == "yes" or default == "y":
        prompt = "[Y/n]"
    elif default == "no" or default == "n":
        prompt = "[y/N]"
    else:
        raise ValueError(f"Invalid default answer: {default}")
    
    # Prompt the user for input
    answer = input(f"{question} {prompt}").lower()
    if default is not None and answer == '':
        if default in valid:
            return valid[default]
        else:
            raise ValueError(f"No mapping found for default of {default}")
    elif answer in valid:
        return valid[answer]
    
    # Invalid choice, re-prompt the user
    return prompt_user_for_yes_or_no(question, default)