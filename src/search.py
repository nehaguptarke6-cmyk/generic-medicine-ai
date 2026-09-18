from langchain_core.documents import Document


def safe_value(value):
    """
    Replace missing values with empty text.
    """

    if value is None:
        return ""

    if str(value).lower() == "nan":
        return ""

    return str(value)


def create_documents(df):
    """
    Convert medicine rows into LangChain Documents.
    """

    documents = []

    for _, row in df.iterrows():

        content = f"""
Medicine Name: {safe_value(row['medicine_name'])}
Generic Name: {safe_value(row['generic_name'])}
Category: {safe_value(row['category'])}
Form: {safe_value(row['form'])}
Description: {safe_value(row['description'])}
Indications: {safe_value(row['indications'])}
Warnings: {safe_value(row['warnings'])}
Adverse Reactions: {safe_value(row['adverse_reactions'])}
Source: {safe_value(row['source'])}
""".strip()

        document = Document(
            page_content=content,
            metadata={
                "medicine_name": safe_value(
                    row["medicine_name"]
                ),
                "source": safe_value(
                    row["source"]
                )
            }
        )

        documents.append(document)

    return documents