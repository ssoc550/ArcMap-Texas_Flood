# Spencer Altus
# Tara Seibold

import arcpy

arcpy.CheckOutExtension(“Spatial”)
arcpy.env.workspace = ???????????????????????????????
arcpy.env.overwriteInput = True

# make feature layer of building footprint shapefile
arcpy.MakeFeatureLayer(in_features = bldg_ftprt, out_layer = bldg_lyr)

# make feature layer of flood depth grid shapefile
arcpy.MakeFeatureLayer(in_features = fld_dpth_grd, out_layer = fld_lyr)

# select buildings from building footprint layer that intersect with flood depth layer
arcpy.SelectLayerByLocation_management(in_layer = bldg_lyr, overlap_type = “INTERSECT”, select_features = fld_lyr, selection_type = "NEW_SELECTION")

# add building area field to building footprint layer
arcpy.AddField_management(in_table = bldg_layer, field_name = "bldg_area", field_type = "float")

# add total damages field to building footprint layer (no data)
arcpy.AddField_management(in_table = bldg_layer, field_name = "tot_dmg", field_type = "float")

# add flood percent damage field to building footprint layer (no data)
arcpy.AddField_management(in_table = bldg_layer, field_name = "fld_pct", field_type = "float")

# add OID field to building footprint layer (no data)
arcpy.AddField_management(in_table = bldg_layer, field_name = "OID1", field_type = "float")

# create shapefile from layer
arcpy.CopyFeatures_management(in_features = bldg_lyr, out_feature_class = bldg_subset)

# create a with statement using a cursor and then create a for loop within the with statement
# to assign area values in square feet to the bldg_area field
with arcpy.da.UpdateCursor(in_table = bldg_subset, field_names = [bldg_area, SHAPE@AREA]) as cursor:
    for row in cursor:
    row[0] = row[1] * (meter to sq. ft. conversion value)
    cursor.UpdateRow(row)

# create a with statement using a cursor
# to assign a permanent OID to each building footprint
# using a for loop within the with statement
with arcpy.da.UpdateCursor(in_table = bldg_subset, field_names = [FID, OID1]) as cursor:
    for row in cursor:
    row[1] = row[0]
    cursor.UpdateRow(row)

# INTERSECT bldg_subset and fld_depth files to assign flood depth values to building footprints
arcpy.Intersect_analysis(in_features = [bldg_subset, fld_dpth_grd], out_feature_class = bldg_fld_intrsct, join_attributes = "ALL")
# DISSOLVE by OID1 but keep all attributes and use MAX for flood depth values
arcpy.Dissolve_management(in_features = bldg_fld_intrsct, out_feature_class = bldg_fld_dsslv, dissolve_field = "OID1", statistics_fields = [fld_dpth, {"MAX"}], multi_part = "SINGLE PART")

# create a with statement using a cursor
# to assign flood depth values to the fld_dpth field
# and then create a for loop to assign damage percent values based on flood depth
# fld_dpth field name will be changed once actual field name determined
with arcpy.da.UpdateCursor(in_table = bldg_fld_dsslv, field_names = [fld_dpth]) as cursor:
    for row in cursor:
        if fld_dpth ISNULL or fld_dpth < 0:
            then fld_pct = 0
# how to we exclude these structures with null fld_dpth fields?
        elif fld_dpth => 0 and fld_dpth < 1:
            then fld_pct = 0.134
        elif fld_dpth => 1 and fld_dpth <2:
            then fld_pct = 0.233
        elif fld_dpth => 2 and fld_dpth < 3:
            then fld_pct = 0.321
        elif fld_dpth => 3 and fld_dpth < 4:
            then fld_pct = 0.401
        elif fld_dpth => 4 and fld_dpth < 5:
            then fld_pct = 0.471
        elif fld_dpth => 5:
            then fld_pct = 0.532
        else fld_dpth ISNULL

# create a with statement using a cursor and then create a for loop within the with statement:
with arcpy.da.UpdateCursor(in_table = bldg_subset, field_names = [bldg_area, fld_pct, tot_dmg]) as cursor:
    for row in cursor:
        row[2] = row[0] * row[1] * 150
        cursor.UpdateRow(row)

# sum and output total structure damage value
# don't think this is correct
total_flood_damages = sum(tot_dmg)
