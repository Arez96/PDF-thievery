import os
import pandas as pd
import requests

input_path = r"C:\Users\SPAC-36\Documents\PDF-thievery\test data\test-data.xlsx"
output_path = r"C:\Users\SPAC-36\Documents\PDF-thievery\test data\output"


def main():
    # Læs Excel
    try:
        df = pd.read_excel(input_path, sheet_name=0)
    except Exception:
        print("GODDAMNIT")
        return
    finally:
        print("test ended")

    # Loop rækker
    for j in range(len(df)):
        file_name = df["BRnum"][j]
        url_link = df["Pdf_URL"][j]

        if type(url_link) is float:  # NaN case
            print("NaN")
            continue

        if type(url_link) is str and os.path.exists(f"{output_path}/{file_name}.pdf") is False:
            try:
                response = requests.get(url_link, allow_redirects=True)
                mime_type = str(response.headers.get("Content-Type"))

                if response.status_code == 200 and mime_type == "application/pdf":
                    print(f"200 : {file_name} / ({mime_type}): Success")
                    save_file = str(file_name + ".pdf")
                    save_dest = os.path.join(output_path, save_file)

                    try:
                        with open(save_dest, "wb") as file:
                            file.write(response.content)
                    except Exception:
                        print(f"Unknown Failure: {save_file}")

                elif response.status_code == 404:
                    print(f"404 : {file_name} : {url_link}")
                else:
                    print("Failure / Not PDF")

            except Exception:
                print(f"exception: {url_link} invalid url")


if __name__ == "__main__":
    main()