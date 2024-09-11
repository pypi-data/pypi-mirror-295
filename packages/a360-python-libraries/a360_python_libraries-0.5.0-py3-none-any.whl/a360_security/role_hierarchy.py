from a360_security.enums.role import Role

ROLE_HIERARCHY = {
    Role.PRACTICE: [],
    Role.ADMIN: ["ROLE_PRACTICE"],
}


def has_role(user_roles: list[str], required_role: Role) -> bool:
    all_roles = set(user_roles)
    roles_to_check = list(user_roles)
    while roles_to_check:
        role = roles_to_check.pop()
        if role in ROLE_HIERARCHY:
            inherited_roles = ROLE_HIERARCHY[role]
            for inherited_role in inherited_roles:
                if inherited_role not in all_roles:
                    all_roles.add(inherited_role)
                    roles_to_check.append(inherited_role)

    return required_role.value in all_roles
