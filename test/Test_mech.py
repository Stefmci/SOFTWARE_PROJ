from classes import mechanismus, save_mechanismus, load_mechanismus

mechanism = mechanismus("Mech1")
mechanism.add_point("A", 0, 0, fixed=True)
mechanism.add_point("B", 10, 10)
mechanism.add_link("A", "B")

save_mechanismus(mechanism)
print("Mechanismus gespeichert!")

loaded_mechanism = load_mechanismus("Mech1")
print("Geladener Mechanismus:", loaded_mechanism.to_dict())


mechanism = mechanismus("Mech2")
mechanism.add_point("C", 0, 0, fixed=True)
mechanism.add_point("D", 10, 10)
mechanism.add_link("C", "D")
save_mechanismus(mechanism)