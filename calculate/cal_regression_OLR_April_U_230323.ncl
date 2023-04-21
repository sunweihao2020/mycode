begin

olr_file  = addfile("/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc", "r")
print(olr_file)
olr_index = olr_file->ttr_avg_mon({1959:2021}, {4})

print(olr_index)

end