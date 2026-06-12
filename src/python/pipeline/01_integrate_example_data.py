import argparse
import sqlite3
import urllib.request
import hashlib
from pathlib import Path
from rdflib import Graph, Namespace, Literal, BNode
from rdflib.namespace import RDF, XSD

def main():
    parser = argparse.ArgumentParser(description="Extract Chinook SQLite to highly detailed, deduplicated RDF.")
    parser.add_argument("--output", type=Path, required=True, help="Output TTL file path")
    args = parser.parse_args()

    db_path = args.output.parent / "chinook.sqlite"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
    
    print(f"Downloading live SQLite database from {url}...")
    try:
        urllib.request.urlretrieve(url, db_path)
    except Exception as e:
        print(f"Failed to download the database: {e}")
        return

    # 1. Initialize Graph and Granular Namespaces
    g = Graph()
    SCHEMA = Namespace("http://schema.org/")
    UNIT = Namespace("http://qudt.org/vocab/unit/")
    
    ARTIST = Namespace("http://example.org/artist/")
    ALBUM = Namespace("http://example.org/album/")
    TRACK = Namespace("http://example.org/tracks/")
    GENRE = Namespace("http://example.org/genre/")
    PLAYLIST = Namespace("http://example.org/playlist/")
    MEDIATYPE = Namespace("http://example.org/mediatype/")
    EMPLOYEE = Namespace("http://example.org/employee/")
    CUSTOMER = Namespace("http://example.org/customer/")
    INVOICE = Namespace("http://example.org/invoice/")
    INVOICELINE = Namespace("http://example.org/invoiceline/")
    ADDRESS = Namespace("http://example.org/address/")

    g.bind("schema", SCHEMA)
    g.bind("unit", UNIT)
    g.bind("artist", ARTIST)
    g.bind("album", ALBUM)
    g.bind("track", TRACK)
    g.bind("genre", GENRE)
    g.bind("playlist", PLAYLIST)
    g.bind("media", MEDIATYPE)
    g.bind("employee", EMPLOYEE)
    g.bind("customer", CUSTOMER)
    g.bind("invoice", INVOICE)
    g.bind("invline", INVOICELINE)
    g.bind("address", ADDRESS)

    print("Connecting to database and minting graph nodes...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # =========================================================================
    # PIPELINE HELPERS
    # =========================================================================

    def add_string(subject, predicate, value):
        """Attaches a plain string literal without a language tag."""
        if value:
            g.add((subject, predicate, Literal(str(value).strip())))

    def add_quantitative_value(subject, predicate, value, datatype, unit_uri):
        """Attaches a schema:QuantitativeValue blank node with a QUDT unit."""
        if value is not None:
            qnode = BNode()
            g.add((subject, predicate, qnode))
            g.add((qnode, RDF.type, SCHEMA.QuantitativeValue))
            g.add((qnode, SCHEMA.value, Literal(value, datatype=datatype)))
            g.add((qnode, SCHEMA.unitCode, unit_uri))

    def build_address(street, city, state, country, postal_code):
        """Generates a deterministic URI for an address based on its contents."""
        fields = [street, city, state, country, postal_code]
        if not any(fields):
            return None
        
        # Create a unique fingerprint by concatenating sanitized strings
        raw_string = "|".join([str(f).strip().lower() for f in fields if f])
        
        # Hash the fingerprint to create a unique, stable identifier
        address_hash = hashlib.md5(raw_string.encode('utf-8')).hexdigest()
        address_uri = ADDRESS[address_hash]
        
        # Assert the address properties
        g.add((address_uri, RDF.type, SCHEMA.PostalAddress))
        add_string(address_uri, SCHEMA.streetAddress, street)
        add_string(address_uri, SCHEMA.addressLocality, city)
        add_string(address_uri, SCHEMA.addressRegion, state)
        add_string(address_uri, SCHEMA.addressCountry, country)
        
        if postal_code:
            g.add((address_uri, SCHEMA.postalCode, Literal(postal_code, datatype=XSD.string)))
            
        return address_uri

    # =========================================================================
    # MUSIC METADATA
    # =========================================================================

    # Artists
    cursor.execute("SELECT ArtistId, Name FROM Artist")
    for row in cursor.fetchall():
        uri = ARTIST[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.MusicGroup))
        add_string(uri, SCHEMA.name, row[1])

    # Albums
    cursor.execute("SELECT AlbumId, Title, ArtistId FROM Album")
    for row in cursor.fetchall():
        uri = ALBUM[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.MusicAlbum))
        add_string(uri, SCHEMA.name, row[1])
        g.add((uri, SCHEMA.byArtist, ARTIST[str(row[2])]))

    # Genres
    cursor.execute("SELECT GenreId, Name FROM Genre")
    for row in cursor.fetchall():
        uri = GENRE[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.DefinedTerm))
        add_string(uri, SCHEMA.name, row[1])

    # Media Types
    cursor.execute("SELECT MediaTypeId, Name FROM MediaType")
    for row in cursor.fetchall():
        uri = MEDIATYPE[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.DefinedTerm))
        add_string(uri, SCHEMA.name, row[1])

    # Tracks
    cursor.execute("""
        SELECT TrackId, Name, AlbumId, MediaTypeId, GenreId, 
               Composer, Milliseconds, Bytes, UnitPrice 
        FROM Track
    """)
    for row in cursor.fetchall():
        uri = TRACK[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.MusicRecording))
        add_string(uri, SCHEMA.name, row[1])
        
        # Express quantitative values via QUDT units
        add_quantitative_value(uri, SCHEMA.duration, row[6], XSD.integer, UNIT.MilliSEC)
        add_quantitative_value(uri, SCHEMA.offers, row[8], XSD.decimal, UNIT.USD)
        
        if row[5]:
            add_string(uri, SCHEMA.author, row[5])
        if row[7] is not None:
            # Cast bytes to an integer quantitative value
            add_quantitative_value(uri, SCHEMA.contentSize, int(row[7]), XSD.integer, UNIT.BYTE)

        if row[2] is not None:
            g.add((uri, SCHEMA.inAlbum, ALBUM[str(row[2])]))
        if row[3] is not None:
            g.add((uri, SCHEMA.encodingFormat, MEDIATYPE[str(row[3])]))
        if row[4] is not None:
            g.add((uri, SCHEMA.genre, GENRE[str(row[4])]))

    # Playlists
    cursor.execute("SELECT PlaylistId, Name FROM Playlist")
    for row in cursor.fetchall():
        uri = PLAYLIST[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.MusicPlaylist))
        add_string(uri, SCHEMA.name, row[1])

    # Playlist-Track mapping
    cursor.execute("SELECT PlaylistId, TrackId FROM PlaylistTrack")
    for row in cursor.fetchall():
        g.add((PLAYLIST[str(row[0])], SCHEMA.track, TRACK[str(row[1])]))

    # =========================================================================
    # ORGANIZATIONAL & COMMERCE DATA
    # =========================================================================

    # Employees
    cursor.execute("""
        SELECT EmployeeId, FirstName, LastName, Title, ReportsTo, 
               BirthDate, HireDate, Address, City, State, Country, PostalCode, Email 
        FROM Employee
    """)
    for row in cursor.fetchall():
        uri = EMPLOYEE[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.Person))
        add_string(uri, SCHEMA.givenName, row[1])
        add_string(uri, SCHEMA.familyName, row[2])
        add_string(uri, SCHEMA.jobTitle, row[3])
        
        if row[5]:
            # Convert SQLite "1970-05-29 00:00:00" to "1970-05-29" and type as xsd:date
            date_only = str(row[5])[:10]
            g.add((uri, SCHEMA.birthDate, Literal(date_only, datatype=XSD.date)))
        if row[12]:
            g.add((uri, SCHEMA.email, Literal(row[12], datatype=XSD.string)))
            
        address_node = build_address(row[7], row[8], row[9], row[10], row[11])
        if address_node:
            g.add((uri, SCHEMA.address, address_node))

        if row[4] is not None:
            g.add((uri, SCHEMA.worksFor, EMPLOYEE[str(row[4])]))

    # Customers
    cursor.execute("""
        SELECT CustomerId, FirstName, LastName, Company, 
               Address, City, State, Country, PostalCode, Email, SupportRepId 
        FROM Customer
    """)
    for row in cursor.fetchall():
        uri = CUSTOMER[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.Person))
        add_string(uri, SCHEMA.givenName, row[1])
        add_string(uri, SCHEMA.familyName, row[2])
        add_string(uri, SCHEMA.worksFor, row[3])
        
        if row[9]:
            g.add((uri, SCHEMA.email, Literal(row[9], datatype=XSD.string)))
            
        address_node = build_address(row[4], row[5], row[6], row[7], row[8])
        if address_node:
            g.add((uri, SCHEMA.address, address_node))

        if row[10] is not None:
            g.add((uri, SCHEMA.knows, EMPLOYEE[str(row[10])]))

    # Invoices
    cursor.execute("""
        SELECT InvoiceId, CustomerId, InvoiceDate, 
               BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total 
        FROM Invoice
    """)
    for row in cursor.fetchall():
        uri = INVOICE[str(row[0])]
        g.add((uri, RDF.type, SCHEMA.Invoice))
        g.add((uri, SCHEMA.customer, CUSTOMER[str(row[1])]))
        
        if row[2]:
            # Convert SQLite "2022-06-22 00:00:00" to "2022-06-22" and type as xsd:date
            date_only = str(row[2])[:10]
            g.add((uri, SCHEMA.dateCreated, Literal(date_only, datatype=XSD.date)))
            
        add_quantitative_value(uri, SCHEMA.totalPaymentDue, row[8], XSD.decimal, UNIT.USD)
        
        address_node = build_address(row[3], row[4], row[5], row[6], row[7])
        if address_node:
            g.add((uri, SCHEMA.billingAddress, address_node))

    # Invoice Lines
    cursor.execute("SELECT InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity FROM InvoiceLine")
    for row in cursor.fetchall():
        uri = INVOICELINE[str(row[0])]
        invoice_uri = INVOICE[str(row[1])]
        
        g.add((uri, RDF.type, SCHEMA.OrderItem))
        g.add((uri, SCHEMA.orderedItem, TRACK[str(row[2])]))
        
        add_quantitative_value(uri, SCHEMA.price, row[3], XSD.decimal, UNIT.USD)
        add_quantitative_value(uri, SCHEMA.orderQuantity, row[4], XSD.integer, UNIT.EA) # 'EA' stands for 'Each'
        
        g.add((invoice_uri, SCHEMA.hasPart, uri))

    conn.close()

    # 3. Serialize standard output
    print(f"Graph fully mapped. Total triples: {len(g)}")
    g.serialize(destination=args.output, format="turtle")
    print(f"Successfully serialized to {args.output}")

if __name__ == "__main__":
    main()