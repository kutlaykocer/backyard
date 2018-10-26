"""The master script."""
import analysis
import storage
import scan


def master_get(form_data):
    """Manage result acquisition."""
    print('[MASTER] call for info on ' + form_data['id'] + ' ...')

    # Check if (valid, up to date) json is already there and if yes, return it
    result = storage.check_storage(form_data)
    if result:
        return result

    # Check if data for analysis is already there and if yes, perform analysis
    result = analysis.perform_analysis(form_data)
    if result:
        return master_get(form_data)

    # Gather reconnessaince data
    while scan.gather_data(form_data) != 'DONE':
        pass
    return master_get(form_data)
