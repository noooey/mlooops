import time
from argparse import ArgumentParser

import psycopg2
import pandas as pd
from sklearn.datasets import load_breast_cancer

def get_data():
	X, y = load_breast_cancer(return_X_y=True, as_frame=True)
	df = pd.concat([X, y], axis="columns")
	rename_rule = {
		"mean radius": "mean_radius",
		"mean texture": "mean_texture",
		"mean perimeter": "mean_perimeter",
		"mean area": "mean_area",
		"mean smoothness": "mean_smoothness",
		"mean compactness": "mean_compactness",
		"mean concavity": "mean_concavity",
		"mean concave points": "mean_concave_points",
		"mean symmetry": "mean_symmetry",
		"mean fractal dimension": "mean_fractal_dimension",
		"radius error": "radius_error",
		"texture error": "texture_error",
		"perimeter error": "perimeter_error",
		"area error": "area_error",
		"smoothness error": "smoothness_error",
		"compactness error": "compactness_error",
		"concavity error": "concavity_error",
		"concave points error": "concave_points_error",
		"symmetry error": "symmetry_error",
		"fractal dimension error": "fractal_dimension_error",
		"worst radius": "worst_radius",
		"worst texture": "worst_texture",
		"worst perimeter": "worst_perimeter",
		"worst area": "worst_area",
		"worst smoothness": "worst_smoothness",
		"worst compactness": "worst_compactness",
		"worst concavity": "worst_concavity",
		"worst concave points": "worst_concave_points",
		"worst symmetry": "worst_symmetry",
		"worst fractal dimension": "worst_fractal_dimension",
	}
	df = df.rename(columns=rename_rule)
	return df

def create_table(db_connect):
	create_table_query = """
	CREATE TABLE IF NOT EXISTS iris_data (
		id SERIAL PRIMARY KEY,
		timestamp timestamp,
		mean_radius float8,
		mean_texture float8,
		mean_perimeter float8,
		mean_area float8,
		mean_smoothness float8,
		mean_compactness float8,
		mean_concavity float8,
		mean_concave_points float8,
		mean_symmetry float8,
		mean_fractal_dimension float8,
		radius_error float8,
		texture_error float8,
		perimeter_error float8,
		area_error float8,
		smoothness_error float8,
		compactness_error float8,
		concavity_error float8,
		concave_points_error float8,
		symmetry_error float8,
		fractal_dimension_error float8,
		worst_radius float8,
		worst_texture float8,
		worst_perimeter float8,
		worst_area float8,
		worst_smoothness float8,
		worst_compactness float8,
		worst_concavity float8,
		worst_concave_points float8,
		worst_symmetry float8,
		worst_fractal_dimension float8,
		target int
	);"""
	print(create_table_query)
	with db_connect.cursor() as cur:
		cur.execute(create_table_query)
		db_connect.commit()

def insert_data(db_connect, data):
	insert_row_query=f"""
	INSERT INTO wisconsin_data (
		timestamp
  		mean_radius,
                mean_texture,
                mean_perimeter,
                mean_area,
                mean_smoothness,
                mean_compactness,
                mean_concavity,
                mean_concave_points,
                mean_symmetry,
                mean_fractal_dimension,
                radius_error,
                texture_error,
                perimeter_error,
                area_error,
                smoothness_error,
                compactness_error,
                concavity_error,
                concave_points_error,
                symmetry_error,
                fractal_dimension_error,
                worst_radius,
                worst_texture,
                worst_perimeter,
                worst_area,
                worst_smoothness,
                worst_compactness,
                worst_concavity,
                worst_concave_points,
                worst_symmetry,
                worst_fractal_dimension,
                target
		)
		VALUES (
			NOW(),
			{data.mean_radius},
			{data.mean_texture},
 			{data.mean_perimeter},
			{data.mean_area},
			{data.mean_smoothness},
			{data.mean_compactness},
			{data.mean_concavity},
			{data.mean_concave_points},
			{data.mean_symmetry},
			{data.mean_fractal_dimension},
			{data.radius_error},
			{data.texture_error},
			{data.perimeter_error},
			{data.area_error},
			{data.smoothness_error},
			{data.compactness_error},
			{data.concavity_error},
			{data.concave_points_error},
			{data.symmetry_error},
			{data.fractal_dimension_error},
			{data.worst_radius},
			{data.worst_texture},
			{data.worst_perimeter},
			{data.worst_area},
			{data.worst_smoothness},
			{data.worst_compactness},
			{data.worst_concavity},
			{data.worst_concave_points},
			{data.worst_symmetry},
			{data.worst_fractal_dimension},
			{data.target}
			);"""
	print(insert_row_query)
	with db_connect.cursor() as cur:
		cur.execute(insert_row_query)
		db_connect.commit()

def generate_data(db_connect, df):
	for i in range(len(df)):
		insert_data(db_connect, df.sample(i).squeeze())
	

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--db-host", dest="db_host", type=str, default="localhost")
	args = parser.parse_args()

	db_connect = psycopg2.connect(
		user="postgres",
		password="0429",
		host=args.db_host,
		port=5432,
		database="postgres",
	)
	create_table(db_connect)
	df = get_data()
	generate_data(db_connect, df)
