import dpdata
#poscar 转为 stru
ls = dpdata.System(file_name='POSCAR',fmt='poscar')
ls.to(file_name="STRU",fmt='abacus/stru')
