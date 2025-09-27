def remove_attributes_from_arff(file_path="training_keyboard.arff"):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Identificar la línea donde terminan los atributos y comienza @DATA
    attribute_index = next(i for i, line in enumerate(lines) if line.strip().upper() == "@DATA")

    # Extraer las líneas de atributos y datos
    attribute_lines = lines[:attribute_index]
    data_lines = lines[attribute_index + 1:]

    # Mantener @RELATION y eliminar @ATTRIBUTE difficulty y @ATTRIBUTE next_score
    attribute_lines = [attribute_lines[0]] + [line for line in attribute_lines[1:] if
                                              not line.startswith("@ATTRIBUTE difficulty") and not line.startswith(
                                                  "@ATTRIBUTE next_score")]

    # Procesar la sección de datos eliminando la primera columna y la penúltima
    updated_data = []
    for line in data_lines:
        parts = line.strip().split(",")
        if len(parts) > 2:  # Asegurar que haya suficientes elementos
            updated_line = ",".join(parts[1:-2] + [parts[-1]])
            updated_data.append(f"{updated_line}\n")

    # Guardar el archivo actualizado
    with open(file_path, "w") as file:
        file.writelines(attribute_lines + ["@DATA\n"] + updated_data)


# Uso de la función
remove_attributes_from_arff()
