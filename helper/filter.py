import pandas as pd

def filterSolver(df, solver):
    return df[df["solvername"] == solver]