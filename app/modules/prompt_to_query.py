import os
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

OPENAI_KEY = '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'
DB_URI = 'sqlite:///./database/sql_app.db'

def convert_prompt_to_query(prompt):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_KEY)
    db_uri = DB_URI
    db = SQLDatabase.from_uri(db_uri)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

    result = db_chain.run(prompt)
    return result


def main():
    user_prompt = input("Enter a prompt: ")

if __name__ == "__main__":
    main()