"""
The helper function(s) for script.py
"""

def assemble_term(spec_name, search_crit):
    """
    Returns the Entrez search term and the search criteria text.
    The function accepts a species name and the user-specified search criteria integer.
    The assembled search term will be used as a search parameter, and the
    search criteria text will be used in the output report.
    """
    if search_crit == 1:
        term = f'"{spec_name}" AND phytoremediation'
        search_crit_txt = " AND phytoremediation"
        return term, search_crit_txt
    if search_crit == 2:
        term = f'"{spec_name}" AND (rhizodegradation OR phytoextraction OR phytostabilization)'
        search_crit_txt = " AND (rhizodegradation OR phytoextraction OR phytostabilization)"
        return term, search_crit_txt
    if search_crit == 3:
        # Add PFAS. Change user prompt as well.
        term = f'"{spec_name}" AND (hydrocarbon OR PAH OR petroleum OR metal OR contaminant)'
        search_crit_txt = " AND (hydrocarbon OR PAH OR petroleum OR metal OR contaminant)"
        return term, search_crit_txt
    if search_crit == 4:
        term = f'"{spec_name}" AND (\"root exudate\" OR rhizosphere OR degradation)'
        search_crit_txt = " AND (root exudate OR rhizosphere OR degradation)"
        return term, search_crit_txt

    # Additional searched added in July. These are meant to expand focus to include "forever chemicals."
    if search_crit == 30:
        term = f'"{spec_name}" AND (hydrocarbon OR PAH OR petroleum OR metal OR contaminant OR pfas)'
        search_crit_txt = " AND (hydrocarbon OR PAH OR petroleum OR metal OR contaminant OR pfas)"
        return term, search_crit_txt
    if search_crit == 5:
        term = f'"{spec_name}" AND (pfas OR perfluoro* OR polyfluoro*)'
        search_crit_txt = " AND (pfas OR perfluoro* OR polyfluoro*)"
        return term, search_crit_txt
    if search_crit == 6:
        term = f'"{spec_name}" AND (fluorocarbons[Mesh] OR pfas[tiab] OR perfluoro*[tiab] OR polyfluoro*[tiab])'
        search_crit_txt = " AND (fluorocarbons[Mesh] OR pfas[tiab] OR perfluoro*[tiab] OR polyfluoro*[tiab])"
        return term, search_crit_txt
