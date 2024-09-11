from invoke import task


@task
def new_feature(ctx, name):
    """Create a new feature folder using Cookiecutter."""
    import inflection
    from cookiecutter.main import cookiecutter

    # Convert name to different naming conventions
    feature_name = inflection.camelize(name)  # Converts to CamelCase
    feature_name_plural = inflection.pluralize(feature_name)  # Pluralizes CamelCase
    feature_snake_case = inflection.underscore(feature_name)  # Converts to snake_case
    feature_snake_case_plural = inflection.underscore(
        feature_name_plural
    )  # Pluralizes snake_case

    # Corrected template URL with HTTPS
    template = "https://github.com/Aventior-Inc/berainSFA-api-cookiecutter"

    # Using Cookiecutter to generate the feature folder
    cookiecutter(
        template=template,
        no_input=True,
        output_dir="api/features/",  # Specifies where to create the new feature folder
        extra_context={
            "feature_name": feature_name,
            "feature_name_plural": feature_name_plural,
            "feature_snake_case": feature_snake_case,
            "feature_snake_case_plural": feature_snake_case_plural,
        },
    )
