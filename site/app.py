from flask import Flask, render_template, json, redirect, jsonify, url_for
from dotenv import load_dotenv, find_dotenv
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

# Configure Flask app
load_dotenv(find_dotenv())
app.config['MYSQL_HOST'] = os.environ.get("DBHOST")
app.config['MYSQL_USER'] = os.environ.get("DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("DBPW")
app.config['MYSQL_DB'] = os.environ.get("DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

#------------------ COUNTRIES ---------------------------#

# Define the route for the countries page
@app.route('/countries')
def countries():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Countries;"
    cur.execute(query)
    countries_data = cur.fetchall()
    cur.close()
    return render_template('countries.html', countries_data=countries_data)

@app.route('/update_country/<int:country_id>', methods=['POST'])
def update_country(country_id):
    try:
        data = request.get_json()
        country_name = data.get('countryName')
        global_region = data.get('globalRegion')
        population = data.get('population')
        # Strip commas from population numbers
        population = population.translate({ord(_): None for _ in ','})
        gdp = data.get('gdp')
        if gdp in ('', 'null', 'Null', 'NULL'):
            gdp = None

        # Update the database record with the new data
        cur = mysql.connection.cursor()
        query = "UPDATE Countries SET countryName=%s, globalRegion=%s, population=%s, gdp=%s WHERE countryID=%s"
        cur.execute(query, (country_name, global_region, population, gdp, country_id))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the update was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the update failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500

# Route for adding country
@app.route('/add_country', methods=['POST'])
def add_country_to_db():
    try:
        # Get the form data from the request
        country_name = request.form.get('countryName')
        global_region = request.form.get('globalRegion')
        population = request.form.get('population')
        # Strip commas from population numbers
        population = population.translate({ord(_): None for _ in ','})
        gdp = request.form.get('gdp')
        inserts = [country_name, global_region, population]
        if gdp in ('', 'null', 'Null', 'NULL'):
            names = '(countryName, globalRegion, population)'
            values = "(%s, %s, %s)"
        else:
            inserts.append(gdp)
            names = '(countryName, globalRegion, population, GDP)'
            values = "(%s, %s, %s, %s)"
        inserts = tuple(inserts)

        # Perform the database insertion here
        cur = mysql.connection.cursor()
        query = f"INSERT INTO Countries {names} VALUES {values}"
        cur.execute(query, inserts)
        mysql.connection.commit()
        cur.close()

        # Redirect to the countries page after successful insertion
        return redirect(url_for('countries'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the country."

# Add a new route to handle deleting a country
@app.route('/delete_country/<int:country_id>', methods=['POST'])
def delete_country(country_id):
    try:
        # Delete the country from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM Countries WHERE countryID=%s"
        cur.execute(query, (country_id,))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the delete was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the delete failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500


#------------------ CONSUMERS ---------------------------#

# Define the route for the consumers page
@app.route('/consumers')
def consumers():
    try:
        # Fetch data from the database for the consumers.html page
        cur = mysql.connection.cursor()
        query = "SELECT * FROM Consumers"
        cur.execute(query)
        consumers_data = cur.fetchall()
        cur.close()
        return render_template('consumers.html', consumers_data=consumers_data)
    except Exception as e:
        # Handle errors appropriately
        print(f"Error: {e}")
        return render_template('error.html')

@app.route('/add_consumer', methods=['POST'])
def add_consumer_to_db():
    try:
        # Get the form data from the request
        municipality = request.form.get('municipality')
        population = request.form.get('population')
        annualConsumption = request.form.get('annualConsumption')

        # Strip commas from large numbers
        population = population.translate({ord(_): None for _ in ','})
        annualConsumption = annualConsumption.translate({ord(_): None for _ in ','})

        inserts = [municipality, population, annualConsumption]
        names = '(municipality, population, annualConsumption)'
        values = '(%s, %s, %s)'
        if annualConsumption in ('', 'null', 'Null', 'NULL'):
            inserts.remove(annualConsumption)
            if population in ('', 'null', 'Null', 'NULL'):
                inserts.remove(population)
                names = '(municipality)'
                values = "(%s)"
            else:
                names = '(municipality, population)'
                values = "(%s, %s)"
        elif population in ('', 'null', 'Null', 'NULL'):
            inserts.remove(population)
            names = '(municipality, annualConsumption)'
            values = "(%s, %s)"

        inserts = tuple(inserts)

        # Perform the database insertion
        cur = mysql.connection.cursor()
        query = f"INSERT INTO Consumers {names} VALUES {values}"
        cur.execute(query, inserts)
        mysql.connection.commit()
        cur.close()

        # Redirect to the consumers page after successful insertion
        return redirect(url_for('consumers'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the consumer."

@app.route('/update_consumer/<int:consumer_id>', methods=['POST'])
def update_consumer(consumer_id):
    try:
        data = request.get_json()
        municipality = data.get('municipality')
        population = data.get('population')
        annual_consumption = data.get('annualConsumption')

        # Handle input format
        if population in ('', 'null', 'Null', 'NULL'):
            population = None
        else:
            population = population.translate({ord(_): None for _ in ','})
        if annual_consumption in ('', 'null', 'Null', 'NULL'):
            annual_consumption = None
        else:
            annual_consumption = annual_consumption.translate({ord(_): None for _ in ','})

        # Update the database record with the new data
        cur = mysql.connection.cursor()
        query = "UPDATE Consumers SET municipality=%s, population=%s, annualConsumption=%s WHERE consumerID=%s"
        cur.execute(query, (municipality, population, annual_consumption, consumer_id))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the update was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the update failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500

@app.route('/delete_consumer/<int:consumer_id>', methods=['POST'])
def delete_consumer(consumer_id):
    try:
        # Delete the consumer from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM Consumers WHERE consumerID=%s"
        cur.execute(query, (consumer_id,))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the delete was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the delete failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500


#------------------ ENERGY TYPES ---------------------------#


# Define the route for the energy_types page
@app.route('/energy_types')
def energy_types():
        # Fetch data from the database for the energy_types.html page
        cur = mysql.connection.cursor()
        query = "SELECT * FROM Energy_Types"
        cur.execute(query)
        energy_types_data = cur.fetchall()
        cur.close()
        return render_template('energy_types.html', energy_types_data=energy_types_data)

@app.route('/add_energy_type_to_db', methods=['POST'])
def add_energy_type_to_db():
    try:
        # Get the form data from the request
        energy_name = request.form.get('energyName')
        emissions_rate = request.form.get('emissionsRate')
        death_rate = request.form.get('deathRate')

        # Strip commas from large numbers
        emissions_rate = emissions_rate.translate({ord(_): None for _ in ','})
        death_rate = death_rate.translate({ord(_): None for _ in ','})

        inserts = [energy_name, emissions_rate, death_rate]
        names = '(energyName, emissionsRate, deathRate)'
        values = '(%s, %s, %s)'
        if emissions_rate in ('', 'null', 'Null', 'NULL'):
            inserts.remove(emissions_rate)
            if death_rate in ('', 'null', 'Null', 'NULL'):
                inserts.remove(death_rate)
                names = '(energyName)'
                values = "(%s)"
            else:
                names = '(energyName, deathRate)'
                values = "(%s, %s)"
        elif death_rate in ('', 'null', 'Null', 'NULL'):
            inserts.remove(death_rate)
            names = '(energyName, emissionsRate)'
            values = "(%s, %s)"

        inserts = tuple(inserts)

        # Perform the database insertion here
        cur = mysql.connection.cursor()
        query = f"INSERT INTO Energy_Types {names} VALUES {values}"
        cur.execute(query, inserts)
        mysql.connection.commit()
        cur.close()

        # Redirect to the energy_types page after successful insertion
        return redirect(url_for('energy_types'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the energy type."

@app.route('/update_energy_type/<int:energy_type_id>', methods=['POST'])
def update_energy_type(energy_type_id):
    try:
        data = request.get_json()
        energy_name = data.get('energyName')
        emissions_rate = data.get('emissionsRate')
        death_rate = data.get('deathRate')

        # Handle input format
        if emissions_rate in ('', 'null', 'Null', 'NULL'):
            emissions_rate = None
        else:
            emissions_rate = emissions_rate.translate({ord(_): None for _ in ','})
        if death_rate in ('', 'null', 'Null', 'NULL'):
            death_rate = None

        # Update the database record with the new data
        cur = mysql.connection.cursor()
        query = "UPDATE Energy_Types SET energyName=%s, emissionsRate=%s, deathRate=%s WHERE energyTypeID=%s"
        cur.execute(query, (energy_name, emissions_rate, death_rate, energy_type_id))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the update was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the update failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500


@app.route('/delete_energy_type/<int:energy_type_id>', methods=['DELETE'])
def delete_energy_type(energy_type_id):
    try:
        # Delete the energy type from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM Energy_Types WHERE energyTypeID=%s"
        cur.execute(query, (energy_type_id,))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the delete was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the delete failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500

#------------------ PROVIDERS ---------------------------#

# Define the route for the providers page
@app.route('/providers')
def providers():
    # Fetch data from the database for the providers.html page
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Providers"
    cur.execute(query)
    providers_data = cur.fetchall()
    cur.close()
    return render_template('providers.html', providers_data=providers_data)

@app.route('/add_provider_to_db', methods=['POST'])
def add_provider_to_db():
    try:
        # Get the form data from the request
        providerName = request.form.get('providerName')
        orgType = request.form.get('orgType')

        # Perform the database insertion here
        cur = mysql.connection.cursor()
        query = f"INSERT INTO Providers (providerName, orgType) VALUES (%s, %s)"
        cur.execute(query, (providerName, orgType))
        mysql.connection.commit()
        cur.close()

        # Redirect to the providers page after successful insertion
        return redirect(url_for('providers'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the provider."

# Define the route for updating a provider's information
@app.route('/update_provider/<int:provider_id>', methods=['POST'])
def update_provider(provider_id):
    try:
        data = request.get_json()
        provider_name = data.get('providerName')
        org_type = data.get('orgType')

        # Update the database record with the new data
        cur = mysql.connection.cursor()
        query = "UPDATE Providers SET providerName=%s, orgType=%s WHERE providerID=%s"
        cur.execute(query, (provider_name, org_type, provider_id))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the update was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the update failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500

# Define the route for deleting a provider
@app.route('/delete_provider/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    try:
        # Delete the provider from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM Providers WHERE providerID=%s"
        cur.execute(query, (provider_id,))
        mysql.connection.commit()
        cur.close()

        # Respond back to the client indicating the delete was successful
        return jsonify({'success': True})
    except Exception as e:
        # If an error occurs, respond back to the client indicating the delete failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500


#---------------------NATIONAL OPERATIONS------------------------#

def just_nap_ops():
    query = "SELECT providerID, countryID " \
            "FROM National_Operations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    national_operations_data = cur.fetchall()
    cur.close()
    return national_operations_data

# Define the route for the national_operations page
@app.route('/national_operations/', methods=['GET', 'POST'])
def national_operations(edit: dict = None):
    country_search = request.form.get('countryName', None)
    if country_search == "":
        country_search = None
    provider_search = request.form.get('providerName', None)
    if provider_search == '':
        provider_search = None

    cur = mysql.connection.cursor()
    query = "SELECT Providers.providerName, Countries.countryName " \
            "FROM Providers " \
            "INNER JOIN National_Operations ON Providers.providerID = National_Operations.providerID " \
            "LEFT JOIN Countries ON National_Operations.countryID = Countries.countryID "
    if country_search is not None and provider_search is not None:
        query += f"WHERE Countries.countryName = '{country_search}' AND Providers.providerName = '{provider_search}';"
    elif provider_search is not None:
        query += f"WHERE Providers.providerName = '{provider_search}';"
    elif country_search is not None:
        query += f"WHERE Countries.countryName = '{country_search}';"
    else:
        query += ";"
    cur.execute(query)
    national_operations_data = cur.fetchall()
    query = "SELECT * FROM Countries ORDER BY countryName DESC;"
    cur.execute(query)
    countries_data = cur.fetchall()
    query = "SELECT * FROM Providers ORDER BY providerName DESC;"
    cur.execute(query)
    providers_data = cur.fetchall()
    cur.close()
    return render_template(
        'national_operations.html',
        national_operations_data=national_operations_data,
        countries_data=countries_data,
        providers_data=providers_data,
        edit_line = edit
    )

# Define the route for the add_national_operator page
@app.route('/add_national_operator/', methods=['POST'])
def add_national_operator():
    try:
        # Get the form data from the request
        providerID = int(request.form.get('providerID'))
        try:
            countryID = int(request.form.get('countryID'))
        except ValueError:
            countryID = None
        if countryID in ('', 'NULL', 'null', 'Null'):
            countryID = None

        # Perform the database insertion here
        cur = mysql.connection.cursor()
        if countryID is None:
            nat_ops = just_nap_ops()
            for nat_op in nat_ops:
                if nat_op["countryID"] is None and nat_op["providerID"] == providerID:
                    raise Exception
            query = "INSERT INTO National_Operations (providerID, countryID) VALUES (%s, %s);"
            cur.execute(query, (providerID, None))
        else:
            query = "INSERT INTO National_Operations (providerID, countryID) VALUES (%s, %s)"
            cur.execute(query, (providerID, countryID))
        mysql.connection.commit()
        cur.close()

        # Redirect to the national_operations page after successful insertion
        return redirect(url_for('national_operations'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the operation."

@app.route('/edit_national_operation/', methods=['POST'])
def edit_national_operation():
    try:
        # Get line to edit
        edit_line = json.loads(request.form.get('row'))
        return national_operations(edit_line)
    except Exception as e:
        # Handle any errors
        print('Error:', str(e))
        return "Could not edit this entry."


@app.route('/update_national_operation/', methods=['POST'])
def update_national_operation():
    try:
        provider_data = json.loads(request.form.get('updateProviderID'))
        provider_id, old_provider_name = int(provider_data["0"]), provider_data["1"]
        country_data = json.loads(request.form.get('updateCountryID'))
        try:
            country_id = int(country_data["0"])
        except ValueError:
            country_id = None
        try:
            old_country_name = str(country_data["1"])
        except ValueError:
            old_country_name = None
        if old_country_name in ("NULL", "", None):
            old_country_name = None
        cur = mysql.connection.cursor()

        # Find country ID if appropriate
        old_country_ID = None
        query = f"SELECT Countries.countryID FROM Countries WHERE Countries.countryName = '{old_country_name}';"
        cur.execute(query)
        countries_data = cur.fetchall()
        try:
            old_country_ID = int(countries_data['0']['countryID'])
        except Exception:
            pass

        # Find provider ID
        query = f"SELECT Providers.providerID " \
                f"FROM Providers " \
                f"WHERE Providers.providerName = '{old_provider_name}';"
        cur.execute(query)
        providers_data = cur.fetchall()
        old_provider_ID = int(providers_data[0]['providerID'])

        # Make updates
        query = f"UPDATE National_Operations " \
                f"SET providerID = %s, countryID = %s " \
                f"WHERE providerID = %s AND countryID = %s;"
        cur.execute(query, (provider_id, country_id, old_provider_ID, old_country_ID))

        mysql.connection.commit()
        cur.close()

        # Redirect to the national_operations page after update
        return redirect(url_for('national_operations'))
    except Exception as e:
        # If an error occurs, respond back to the client indicating the update failed
        print('Error:', str(e))
        return jsonify({'success': False}), 500


#---------------------PROVIDER ENERGY TYPES------------------------#

@app.route('/provider_energy_types', methods=['GET', 'POST'])
def provider_energy_types():
    provider_name_filter = request.form.get('providerName')
    energy_type_filter = request.form.get('energyType')

    cur = mysql.connection.cursor()
    query = "SELECT Providers.providerName, Energy_Types.energyName " \
            "FROM Providers " \
            "INNER JOIN Provider_Energy_Types ON Providers.providerID = Provider_Energy_Types.providerID " \
            "INNER JOIN Energy_Types ON Provider_Energy_Types.energyTypeID = Energy_Types.energyTypeID "

    if provider_name_filter:
        query += f"WHERE Providers.providerName = '{provider_name_filter}' "
    if energy_type_filter:
        if provider_name_filter:
            query += "AND "
        else:
            query += "WHERE "
        query += f"Energy_Types.energyName = '{energy_type_filter}' "

    query += "ORDER BY Providers.providerName, Energy_Types.energyName;"
    cur.execute(query)
    provider_energy_types_data = cur.fetchall()

    query = "SELECT * FROM Providers ORDER BY providerName DESC;"
    cur.execute(query)
    providers_data = cur.fetchall()

    query = "SELECT * FROM Energy_Types ORDER BY energyName DESC;"
    cur.execute(query)
    energy_types_data = cur.fetchall()

    cur.close()

    return render_template(
        'provider_energy_types.html',
        provider_energy_types_data=provider_energy_types_data,
        providers_data=providers_data,
        energy_types_data=energy_types_data,
    )


# Define the route for adding provider energy types
@app.route('/add_provider_energy_type', methods=['POST'])
def add_provider_energy_type():
    try:
        # Get the form data from the request
        providerID = request.form.get('providerID')
        energyTypeID = request.form.get('energyTypeID')

        # Perform the database insertion here
        cur = mysql.connection.cursor()
        query = "INSERT INTO Provider_Energy_Types (providerID, energyTypeID) VALUES (%s, %s)"
        cur.execute(query, (providerID, energyTypeID))
        mysql.connection.commit()
        cur.close()

        # Redirect to the provider_energy_types page after successful insertion
        return redirect(url_for('provider_energy_types'))
    except Exception as e:
        # Handle any errors that occur during insertion
        print('Error:', str(e))
        return "An error occurred while adding the energy type."

#---------------------ENERGY PROVISIONS------------------------#

@app.route('/energy_provisions', methods=['GET', 'POST'])
def energy_provisions(edit: tuple = None):
    cur = mysql.connection.cursor()
    query = "SELECT Providers.providerName AS company, Consumers.municipality, Energy_Types.energyName " \
            "FROM Energy_Provisions " \
            "INNER JOIN Providers ON Energy_Provisions.providerID = Providers.providerID " \
            "INNER JOIN Consumers ON Energy_Provisions.consumerID = Consumers.consumerID " \
            "INNER JOIN Energy_Types ON Energy_Provisions.energyTypeID = Energy_Types.energyTypeID "
    cur.execute(query)
    energy_provisions_data = cur.fetchall()

    cur = mysql.connection.cursor()
    query = "SELECT Energy_Provisions.providerID AS company, Consumers.municipality, Energy_Types.energyName " \
            "FROM Energy_Provisions " \
            "INNER JOIN Consumers ON Energy_Provisions.consumerID = Consumers.consumerID " \
            "INNER JOIN Energy_Types ON Energy_Provisions.energyTypeID = Energy_Types.energyTypeID " \
            "WHERE Energy_Provisions.providerID = NULL"
    cur.execute(query)
    null_providers = cur.fetchall()

    energy_provisions_data += null_providers

    query = "SELECT * FROM Providers ORDER BY providerName DESC;"
    cur.execute(query)
    providers_data = cur.fetchall()

    query = "SELECT * FROM Consumers ORDER BY municipality DESC;"
    cur.execute(query)
    consumers_data = cur.fetchall()

    query = "SELECT * FROM Energy_Types ORDER BY energyName DESC;"
    cur.execute(query)
    energy_types_data = cur.fetchall()

    cur.close()

    return render_template(
        'energy_provisions.html',
        energy_provisions_data=energy_provisions_data,
        providers_data=providers_data,
        consumers_data=consumers_data,
        energy_types_data=energy_types_data,
        edit_line=edit
    )

@app.route('/add_provision', methods=['POST'])
def add_provision():
    form_submitted = False
    success_message = None
    error_message = None

    provider_id = request.form.get('providerID')
    consumer_id = request.form.get('consumerID')
    energy_type_id = request.form.get('energyTypeID')

    try:
        cur = mysql.connection.cursor()
        if provider_id == '':
            query = "INSERT INTO Energy_Provisions (consumerID, energyTypeID) VALUES (%s, %s)"
            cur.execute(query, (consumer_id, energy_type_id))
        else:
            query = "INSERT INTO Energy_Provisions (providerID, consumerID, energyTypeID) VALUES (%s, %s, %s)"
            cur.execute(query, (provider_id, consumer_id, energy_type_id))
        mysql.connection.commit()
        cur.close()

        success_message = 'Energy provision added successfully'
    except Exception as e:
        print('Error:', str(e))
        error_message = 'Failed to add energy provision'

        form_submitted = True

    cur = mysql.connection.cursor()
    query = "SELECT * FROM Providers ORDER BY providerName DESC;"
    cur.execute(query)
    providers_data = cur.fetchall()

    query = "SELECT * FROM Consumers ORDER BY municipality DESC;"
    cur.execute(query)
    consumers_data = cur.fetchall()

    query = "SELECT * FROM Energy_Types ORDER BY energyName DESC;"
    cur.execute(query)
    energy_types_data = cur.fetchall()

    cur.close()

    return redirect(url_for('energy_provisions'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 55340))
    #app.run(port=port, debug=True)
    app.run(port=8000, debug=True, host='127.0.0.1')
