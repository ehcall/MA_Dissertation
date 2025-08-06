from Cleaning_Programs import adding_headings, adding_sections, locating_quotes, modifying_quotations
from Data_Analysis_Programs import quote_data, keywords
def do_cleaning():
    print("...Adding headings")
    adding_headings.main()
    print("...Adding sections")
    adding_sections.main()
    print("...Locating quotes")
    locating_quotes.main()
    print("...Modifying quotations")
    modifying_quotations.main()
    return

def do_analysis():
    print("...Fetching quote data")
    quote_data.main()
    print("...Doing keyword things")
    keywords.main()

    return


#do_cleaning()
do_analysis()