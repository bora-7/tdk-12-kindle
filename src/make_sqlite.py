import json
import sqlite3

if __name__ == "__main__":
    data = []
    with open("../tdk12/tdk-12.json", "r", encoding="utf-8") as file:
        all_entries = json.load(file)
        for entry in all_entries:
            word = entry["madde"]
            if "anlamlarListe" in entry:
                meanings = [anlam["anlam"] for anlam in entry["anlamlarListe"]]
            else:
                print(entry)
                continue
            data.append((word, "|".join(meanings)))

    print(data)
    conn = sqlite3.connect("dictionary.db")
    cursor = conn.cursor()

    cursor.execute(
        """
      CREATE TABLE IF NOT EXISTS dictionary (
          word TEXT PRIMARY KEY,
          meanings TEXT
      )
  """
    )

    cursor.executemany(
        "INSERT OR REPLACE INTO dictionary (word, meanings) VALUES (?, ?)", data
    )
    conn.commit()

    # Close the database connection
    conn.close()
