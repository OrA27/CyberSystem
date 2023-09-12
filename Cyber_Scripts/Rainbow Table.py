import rainbowtables as rt


def create_table(wordlists, path="/rainbow_tables", file_name="rainbow_table", hash_type="sha256"):
    rt.set_directory(path, full_path=False)
    rt.set_filename(file_name)

    rt.create_directory()
    rt.create_file()
    rt.insert_wordlists(wordlists, hash_type, wordlist_encoding="utf-8", display_progress=True, compression=True)


def hash_lookup(hashed, table="rainbow_table"):
    lookup = rt.search(hashed, table, full_path=True, time_took=True, compression=True)
    return lookup


def execute(hashed, table="rainbow_table"):
    # table creation should happen prior to execution ??

    # extract relevant username and hashed password from db or from GUI

    # lookup the hash in the table
    res = hash_lookup(hashed, table)

    # lookup successful -> go through login flow
    # open up login page

    # input username and plaintext

    # perform login

    # lookup failed -> abort
