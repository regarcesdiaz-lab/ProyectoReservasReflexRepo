"""
Script para poblar la base de datos con datos de prueba.

Crea:
- 1 usuario admin (admin@turismodo.com / admin123)
- 1 usuario cliente de prueba (cliente@test.com / cliente123)
- 6 ofertas turísticas dominicanas

Uso: python seed.py
"""
import reflex as rx
from ProyectoReservasReflex.models.usuario import Usuario
from ProyectoReservasReflex.models.oferta import Oferta
from ProyectoReservasReflex.utils.auth import hash_password


usuarios_demo = [
    {
        "nombre": "Admin",
        "apellido": "Sistema",
        "email": "admin@turismodo.com",
        "telefono": "+18095550100",
        "password_hash": hash_password("admin123"),
        "rol": "admin",
    },
    {
        "nombre": "Cliente",
        "apellido": "Prueba",
        "email": "cliente@test.com",
        "telefono": "+18095550200",
        "password_hash": hash_password("cliente123"),
        "rol": "cliente",
    },
]


ofertas_demo = [
    {
        "titulo": "Punta Cana – 5 días todo incluido",
        "destino": "Punta Cana",
        "descripcion": "Resort 5 estrellas frente al mar, comidas y bebidas ilimitadas.",
        "descripcion_larga": (
            "Disfruta de cinco días en uno de los mejores resorts de Punta Cana. "
            "Tendrás acceso ilimitado a buffets internacionales, restaurantes a la "
            "carta, bares en la playa y actividades acuáticas. El paquete incluye "
            "habitación con vista al mar, traslados desde el aeropuerto y servicio "
            "de concierge personalizado."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "precio": 850.00,
        "duracion_dias": 5,
        "itinerario": (
            "Día 1: Llegada al aeropuerto, traslado al hotel, cóctel de bienvenida.\n"
            "Día 2: Día libre en la playa de Bávaro. Cena temática italiana.\n"
            "Día 3: Excursión a la Isla Saona (almuerzo incluido).\n"
            "Día 4: Spa y snorkeling en el arrecife. Cena romántica.\n"
            "Día 5: Desayuno y traslado al aeropuerto."
        ),
        "incluye": "Vuelo, hotel 5★, todas las comidas, traslados, excursiones",
    },
    {
        "titulo": "Samaná – Aventura en la naturaleza",
        "destino": "Samaná",
        "descripcion": "Avistamiento de ballenas, Cayo Levantado y Cascada El Limón.",
        "descripcion_larga": (
            "Tres días en la península de Samaná, uno de los paraísos naturales "
            "más impresionantes del Caribe. Verás ballenas jorobadas (en temporada), "
            "te bañarás en la cascada El Limón y navegarás hasta el famoso Cayo Bacardí."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
        "precio": 420.00,
        "duracion_dias": 3,
        "itinerario": (
            "Día 1: Llegada a Samaná, paseo por el pueblo, cena de mariscos.\n"
            "Día 2: Avistamiento de ballenas en bote + Cayo Levantado.\n"
            "Día 3: Cabalgata y cascada El Limón. Regreso."
        ),
        "incluye": "Hotel boutique, desayunos, transporte, guías, excursiones",
    },
    {
        "titulo": "Santo Domingo Colonial – City Tour Cultural",
        "destino": "Santo Domingo",
        "descripcion": "Recorre la primera ciudad del Nuevo Mundo en 2 días.",
        "descripcion_larga": (
            "Conoce la historia viva de América en la Zona Colonial, declarada "
            "Patrimonio de la Humanidad por la UNESCO. Visitarás la Catedral "
            "Primada de América, el Alcázar de Colón y los Tres Ojos."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=800",
        "precio": 220.00,
        "duracion_dias": 2,
        "itinerario": (
            "Día 1: Tour por la Zona Colonial, Alcázar de Colón, almuerzo típico.\n"
            "Día 2: Los Tres Ojos, mercado modelo, malecón al atardecer."
        ),
        "incluye": "Hotel colonial, desayunos, guía bilingüe, entradas",
    },
    {
        "titulo": "Jarabacoa – Ecoturismo y rafting",
        "destino": "Jarabacoa",
        "descripcion": "Rafting, parapente y cascadas en las montañas dominicanas.",
        "descripcion_larga": (
            "Tres días de pura adrenalina en la zona montañosa más bella del país. "
            "Practicarás rafting en el río Yaque del Norte, salto en parapente y "
            "visitarás las cascadas de Jimenoa y Baiguate."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1533873984035-25970ab07461?w=800",
        "precio": 380.00,
        "duracion_dias": 3,
        "itinerario": (
            "Día 1: Llegada, recorrido por el pueblo, cena criolla.\n"
            "Día 2: Rafting en el Yaque del Norte + parapente.\n"
            "Día 3: Cascadas Jimenoa y Baiguate. Regreso."
        ),
        "incluye": "Cabaña, comidas, equipo de aventura, transporte, guías",
    },
    {
        "titulo": "Bayahíbe – Buceo y Saona",
        "destino": "Bayahíbe",
        "descripcion": "Buzos certificados explorarán arrecifes y barcos hundidos.",
        "descripcion_larga": (
            "Cuatro días en uno de los mejores destinos de buceo del Caribe. "
            "Tendrás dos inmersiones diarias en arrecifes de coral, una visita "
            "al barco hundido Astron y un día completo en la paradisíaca Isla Saona."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=800",
        "precio": 690.00,
        "duracion_dias": 4,
        "itinerario": (
            "Día 1: Llegada, check-in en hotel frente al mar.\n"
            "Día 2: Dos inmersiones de buceo + cena en la playa.\n"
            "Día 3: Excursión a Isla Saona con almuerzo.\n"
            "Día 4: Inmersión al barco Astron. Regreso."
        ),
        "incluye": "Hotel, comidas, equipo de buceo, instructor, excursiones",
    },
    {
        "titulo": "Constanza – Escapada de invierno",
        "destino": "Constanza",
        "descripcion": "Los valles más fríos del Caribe, ideal para amantes de la naturaleza.",
        "descripcion_larga": (
            "Dos días en el 'Suiza del Caribe'. Disfruta de temperaturas frescas, "
            "campos de flores, fresas frescas y paisajes de pinos. Incluye visita "
            "al Salto de Aguas Blancas y al Valle Nuevo."
        ),
        "imagen_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
        "precio": 195.00,
        "duracion_dias": 2,
        "itinerario": (
            "Día 1: Llegada, tour por campos de flores y fresas.\n"
            "Día 2: Salto de Aguas Blancas, Valle Nuevo, regreso."
        ),
        "incluye": "Cabaña con chimenea, desayunos, guía local, transporte",
    },
]


def main():
    print("=" * 60)
    print("Poblando base de datos...")
    print("=" * 60)

    with rx.session() as session:
        # === Usuarios ===
        usuarios_existentes = session.exec(Usuario.select()).all()
        if usuarios_existentes:
            print(f"⚠ Ya hay {len(usuarios_existentes)} usuarios en la BD.")
            r = input("¿Borrarlos y crear los de prueba? (s/n): ").lower()
            if r == "s":
                for u in usuarios_existentes:
                    session.delete(u)
                session.commit()
                print("✓ Usuarios anteriores eliminados.")
            else:
                print("ℹ Manteniendo usuarios existentes.")
                # Verificar que existe el admin
                admin = session.exec(
                    Usuario.select().where(Usuario.email == "admin@turismodo.com")
                ).first()
                if not admin:
                    print("⚠ No existe el admin. Creándolo...")
                    session.add(Usuario(**usuarios_demo[0]))
                    session.commit()
                    print("✓ Admin creado.")
        if not session.exec(Usuario.select()).first():
            print(f"Creando {len(usuarios_demo)} usuarios de prueba...")
            for u in usuarios_demo:
                session.add(Usuario(**u))
            session.commit()
            print("✓ Usuarios creados:")
            print("    admin@turismodo.com / admin123 (ADMIN)")
            print("    cliente@test.com / cliente123 (CLIENTE)")

        # === Ofertas ===
        ofertas_existentes = session.exec(Oferta.select()).all()
        if ofertas_existentes:
            print(f"\n⚠ Ya hay {len(ofertas_existentes)} ofertas en la BD.")
            r = input("¿Borrarlas y crear las de prueba? (s/n): ").lower()
            if r == "s":
                for o in ofertas_existentes:
                    session.delete(o)
                session.commit()
                print("✓ Ofertas anteriores eliminadas.")
            else:
                print("ℹ Manteniendo ofertas existentes.")
                print("=" * 60)
                print("✓ Seed completado.")
                return

        print(f"\nInsertando {len(ofertas_demo)} ofertas...")
        for datos in ofertas_demo:
            session.add(Oferta(**datos))
        session.commit()
        print(f"✓ {len(ofertas_demo)} ofertas creadas con éxito.")

    print("=" * 60)
    print("✓ Seed completado.")
    print("=" * 60)
    print("\nPuedes entrar con:")
    print("  Admin   → admin@turismodo.com   / admin123")
    print("  Cliente → cliente@test.com      / cliente123")


if __name__ == "__main__":
    main()
