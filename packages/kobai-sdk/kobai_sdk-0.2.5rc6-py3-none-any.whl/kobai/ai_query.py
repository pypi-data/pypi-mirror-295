from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks
from langchain.globals import set_debug

MESSAGE_SYSTEM_TEMPLATE = """
    You are a data analyst tasked with answering questions based on a provided data set. Please answer the questions based on the provided context below. Make sure not to make any changes to the context, if possible, when preparing answers to provide accurate responses. If the answer cannot be found in context, just politely say that you do not know, do not try to make up an answer.
    When you receive a question from the user, answer only that one question in a concise manner. Do not elaborate with other questions.
    """

MESSAGE_AI_TEMPLATE = """
    The table information is as follows:
    {table_data}
    """

MESSAGE_USER_CONTEXT_TEMPLATE = """
    The context being provided is from a table named: {table_name}
    """

MESSAGE_USER_QUESTION_TEMPLATE = """
    {question}
    """

SIMPLE_PROMPT_TEMPLATE = f"""
    {MESSAGE_SYSTEM_TEMPLATE}

    {MESSAGE_USER_CONTEXT_TEMPLATE}

    {MESSAGE_AI_TEMPLATE}

    Question: {MESSAGE_USER_QUESTION_TEMPLATE}
    """


def followup_question(question, data, question_name, override_model=None, use_simple_prompt=False, debug=False):

    set_debug(debug)

    if override_model is None:
        chat_model = ChatDatabricks(
            endpoint="databricks-dbrx-instruct"
            )
    else:
        chat_model=override_model

    if use_simple_prompt:
        prompt = PromptTemplate.from_template(SIMPLE_PROMPT_TEMPLATE)
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(MESSAGE_SYSTEM_TEMPLATE),
                HumanMessagePromptTemplate.from_template(MESSAGE_USER_CONTEXT_TEMPLATE),
                AIMessagePromptTemplate.from_template(MESSAGE_AI_TEMPLATE),
                HumanMessagePromptTemplate.from_template(MESSAGE_USER_QUESTION_TEMPLATE)
            ]
        )

    output_parser = StrOutputParser()

    chain = prompt | chat_model | output_parser

    response = chain.invoke(
        {
            "table_name": question_name,
            "table_data": str(data),
            "question": question
        }
    )

    return response


