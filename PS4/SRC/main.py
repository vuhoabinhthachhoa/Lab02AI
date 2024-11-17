def parse_input(filename="input1.txt"):
    with open(filename, "r") as f:
        alpha = f.readline().strip()  # The alpha statement
        num_clauses = int(f.readline().strip())
        kb = [set(line.strip().split(" OR ")) for line in f.readlines()]
    
    # Negate alpha and add it to the knowledge base as ~alpha
    neg_alpha = set()
    for lit in alpha.split(" OR "):
        neg_alpha.add('-' + lit if lit[0] != '-' else lit[1:])
    kb.append(neg_alpha)

    return kb, alpha

def resolve(clause1, clause2):
    resolvents = set()
    for literal in clause1:
        # Find complements between clauses
        if ('-' + literal) in clause2 or (literal[1:] if literal.startswith('-') else '-' + literal) in clause2:
            # Resolve clauses without this pair of complementary literals
            new_clause = (clause1 - {literal}) | (clause2 - {('-' + literal) if literal[0] != '-' else literal[1:]})
            # Remove tautologies e.g., {A, -A}
            if not any(lit in new_clause and ('-' + lit if lit[0] != '-' else lit[1:]) in new_clause for lit in new_clause):
                resolvents.add(frozenset(new_clause))
    return resolvents

def pl_resolution(kb):
    new_clauses = set()
    clauses = set(map(frozenset, kb))
    loop_results = []

    while True:
        new = set()
        # Collect all pairs of clauses
        pairs = [(c1, c2) for i, c1 in enumerate(clauses) for c2 in list(clauses)[i + 1:]]
        
        for (c1, c2) in pairs:
            resolvents = resolve(c1, c2)
            if frozenset() in resolvents:  # Empty clause found
                loop_results.append((len(new), list(new)))
                with open("output.txt", "w") as out_file:
                    for loop, clauses in loop_results:
                        out_file.write(f"{loop}\n" + "\n".join(" OR ".join(sorted(clause)) for clause in clauses) + "\n")
                    out_file.write("YES\n")
                return True
            
            new = new | resolvents

        # Record current loop results
        loop_results.append((len(new), list(new)))

        # Check if new information was added
        if new.issubset(clauses):
            with open("output.txt", "w") as out_file:
                for loop, clauses in loop_results:
                    out_file.write(f"{loop}\n" + "\n".join(" OR ".join(sorted(clause)) for clause in clauses) + "\n")
                out_file.write("NO\n")
            return False

        clauses = clauses | new

def main():
    kb, alpha = parse_input("input1.txt")
    entailment = pl_resolution(kb)
    print("KB entails α:", entailment)

if __name__ == "__main__":
    main()
