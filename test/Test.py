from queries import save_points, get_all_points, delete_points, find_points, delete_all_points

save_points("A", 10, 20, fixed=True)
save_points("B", -5, 15, fixed=False)

print("Gespeichert:", get_all_points())

delete_points("A")
print("Nach Löschen:", find_points())

print("Verbleibenden Punkte:", get_all_points())

delete_all_points()

print("Alles löschen:", find_points())