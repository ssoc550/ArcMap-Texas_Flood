# Spencer Altus
# Tara Seibold

import arcpy
from arcpy import env
from arcpy.sa import *


# For Spencer's remove # from this line:
# arcpy.env.workspace = r'S:\GEOG_4308.80_Programming_Geospatial_202001\Altus,Spencer-SAltus\Final_Project\texas_shape\god_help_us.shp'
# This is Tara's workspace
arcpy.env.workspace = r'S:\GEOG_6308.80_Programming_Geospatial_202001\Seibold,Tara-TSeibold\Final_Project'
arcpy.env.scratchWorkspace = r'S:\GEOG_6308.80_Programming_Geospatial_202001\Seibold,Tara-TSeibold\Final_Project'
arcpy.env.overwriteOutput = True

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension("Spatial")

#%%
# Spencer's
# bldg_ftprt = r'S:\GEOG_4308.80_Programming_Geospatial_202001\Altus,Spencer-SAltus\Final_Project\texas_shape\god_help_us.shp'
# Tara's
bldg_ftprt = r'S:\GEOG_6308.80_Programming_Geospatial_202001\Seibold,Tara-TSeibold\Final_Project\texas_shape\TX_bldg_clip.shp'

#%%
# Spencer's:
# fld_dpth_ras =
# Tara's
fld_dpth_ras = arcpy.Raster(r'S:\GEOG_6308.80_Programming_Geospatial_202001\Seibold,Tara-TSeibold\Final_Project\fld_ras_clip3')
fld_dpth_ras = Int(in_raster_or_constant = fld_dpth_ras)
fld_dpth_ras = MajorityFilter(in_raster = fld_dpth_ras, number_neighbors = "FOUR", majority_definition = "HALF")

#%%
# Replaces cells in a raster based on the majority of their contiguous neighboring cells
fld_dpth_ras = MajorityFilter(in_raster = fld_dpth_ras, number_neighbors = "FOUR", majority_definition = "HALF")

#%%
# ranges should not overlap except at the boundary
fld_dpth_ras = Reclassify(in_raster = fld_dpth_ras, reclass_field = "Value", remap = RemapRange([[-1000, 0, -1], [0.01, 1, 0], [1.01, 2, 1], [2.01, 3, 2],[3.01, 4, 3], [4.01, 5, 4], [5.01, 45, 5]]), missing_values = "NODATA")
arcpy.RasterToPolygon_conversion(in_raster = fld_dpth_ras, out_polygon_features = "fld_dpth_grd.shp", simplify = "SIMPLIFY", create_multipart_features = "MULTIPLE_OUTER_PART")

#%%
# make feature layer of building footprint shapefile
arcpy.MakeFeatureLayer_management(in_features = bldg_ftprt, out_layer = "bldg_lyr")

bldg_count = arcpy.GetCount_management("bldg_lyr")
print bldg_count

#%%

# make feature layer of flood depth grid shapefile
arcpy.MakeFeatureLayer_management(in_features = "fld_dpth_grd.shp", out_layer = "fld_lyr")
fld_count = arcpy.GetCount_management("fld_lyr")
print fld_count

#%%
# arcpy.AddField_management(in_table = "fld_lyr", field_name = "dissolve", field_type = "short")

#with arcpy.da.UpdateCursor(in_table = "fld_lyr", field_names = ["dissolve"]) as cursor:
#    for row in cursor:
#        row[0] = 1
#        cursor.updateRow(row)
#
#arcpy.Dissolve_management(in_features = "fld_lyr", out_feature_class= "fld_dissolve", dissolve_field = "dissolve")

##%%
## select buildings from building footprint layer that intersect with flood depth layer
## in theory if Citrix could handle it
#arcpy.MakeFeatureLayer_management(in_features = "fld_dissolve", out_layer = "fld_intersect")
#
#arcpy.SelectLayerByLocation_management(in_layer = "bldg_lyr", overlap_type = "INTERSECT", select_features = "fld_intersect", selection_type = "NEW_SELECTION")

#%%
# add building area field to building footprint layer
arcpy.AddField_management(in_table = "bldg_lyr", field_name = "bldg_area", field_type = "float")
#%%

# add total damages field to building footprint layer (no data)
arcpy.AddField_management(in_table = "bldg_lyr", field_name = "tot_dmg", field_type = "float")

#%%
# add flood percent damage field to building footprint layer (no data)
arcpy.AddField_management(in_table = "bldg_lyr", field_name = "fld_pct", field_type = "float")

#%%
# add OID field to building footprint layer (no data)
arcpy.AddField_management(in_table = "bldg_lyr", field_name = "OID1", field_type = "float")

#%%
bldg_count = arcpy.GetCount_management("bldg_lyr")
print bldg_count

#%%
# create shapefile from layer
arcpy.CopyFeatures_management(in_features = "bldg_lyr", out_feature_class = "bldg_subset3")

#%%
bldg_count = arcpy.GetCount_management("bldg_subset3.shp")
print bldg_count

#%%
# create shapefile from layer
# arcpy.CopyFeatures_management(in_features = "fld_lyr", out_feature_class = "fld_ply")

#%%
#bldg_subset_count = arcpy.GetCount_management("bldg_subset2")
#print bldg_subset_count

#%%
#
## create a with statement using a cursor and then create a for loop within the with statement
## to assign area values in square feet to the bldg_area field
#with arcpy.da.UpdateCursor(in_table = "bldg_lyr", field_names = ["bldg_area", "SHAPE@AREA"]) as cursor:
#    for row in cursor:
#        row[0] = row[1]
#        cursor.updateRow(row)
        
#%%
# create a with statement using a cursor
# to assign a permanent OID to each building footprint
# using a for loop within the with statement
with arcpy.da.UpdateCursor(in_table = "bldg_subset3.shp", field_names = ["FID", "OID1"]) as cursor:
    for row in cursor:
        row[1] = row[0]
        cursor.updateRow(row)  

#%%
# arcpy.MakeFeatureLayer_management(in_features = "bldg_subset.shp", out_layer = "bldg_subset_lyr")

#%%
bldg_count = arcpy.GetCount_management("bldg_subset3.shp")
print bldg_count
#%%
fld_count =arcpy.GetCount_management("fld_dpth_grd.shp")
print fld_count

#%%
# INTERSECT bldg_subset and fld_depth files to assign flood depth values to building footprints
arcpy.Intersect_analysis(in_features = ["bldg_subset3.shp", "fld_dpth_grd.shp"], out_feature_class = "bldg_fld_ply.shp", join_attributes = "ALL")

#%%

# DISSOLVE by OID1 but keep all attributes and use MAX for flood depth values
arcpy.Dissolve_management(in_features = "bldg_fld_ply", out_feature_class = "bldg_fld_dsslv", dissolve_field = "OID1", statistics_fields = ["gridcode", {"MAX"}], multi_part = "SINGLE_PART")

#%%

# create a with statement using a cursor and then create a for loop within the with statement
# to assign area values in square feet to the bldg_area field
with arcpy.da.UpdateCursor(in_table = "bldg_fld_dsslv", field_names = ["bldg_area", "SHAPE@AREA"]) as cursor:
    for row in cursor:
        row[0] = row[1]
        cursor.updateRow(row)
#%%
# create a with statement using a cursor
# to assign flood depth values to the fld_dpth field
# and then create a for loop to assign damage percent values based on flood depth
# fld_dpth field name will be changed once actual field name determined
with arcpy.da.UpdateCursor(in_table = "bldg_fld_dsslv", field_names = ["gridcode", "fld_pct"]) as cursor:
    for row in cursor:
        if row[0] < 0:
            row[1] = 0
# how to we exclude these structures with null fld_dpth fields?
        elif row[0] == 0:
            row[1] = 0.134
        elif row[0] == 1:
            row[1] = 0.233
        elif row[0] == 2:
            row[1] = 0.321
        elif row[0] == 3:
            row[1] = 0.401
        elif row[0] == 4:
            row[1] = 0.471
        elif row[0] == 5:
            row[1] = 0.532
        else:
            row[1] == 0
        cursor.updateRow(row)

#%%
# create a with statement using a cursor and then create a for loop within the with statement:
with arcpy.da.UpdateCursor(in_table = "bldg_fld_dsslv", field_names = ["bldg_area", "fld_pct", "tot_dmg"]) as cursor:
    for row in cursor:
        row[2] = row[0] * row[1] * 150 * 10.7639
        cursor.updateRow(row)

#%%
# sum and output total structure damage value
# arcpy.Statistics_analysis(in_table, out_table, statistics_fields, {case_field}) 
# statistics_fields = [[field, statistics_type]...]
arcpy.Statistics_analysis(in_table = "bldg_fld_dsslv.shp", out_table = "total_damage_table", statistics_fields =["tot_dmg", "SUM"])


