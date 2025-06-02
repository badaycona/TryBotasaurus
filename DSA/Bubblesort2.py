appoinments = [('Nam', '14:30'), ('Linh','09:15'), ('Hung','12:00'), ('An','08:45'), ('MaI','10:20')]
def time_conversion(s : str):
    return int(s[:2])*60 + int(s[3:])
for i in range(len(appoinments)):
    for j in range(i, len(appoinments)):
        if time_conversion(appoinments[j][1]) < time_conversion(appoinments[i][1]):
            appoinments[i], appoinments[j] = appoinments[j], appoinments[i]
print(appoinments)
