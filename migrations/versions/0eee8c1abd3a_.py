"""empty message

Revision ID: 0eee8c1abd3a
Revises: fcd9cebaa79c
Create Date: 2019-05-24 23:05:45.512395

"""
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa

import json
from geoalchemy2.shape import to_shape
from shapely.geometry import shape
import shapely.wkt



# revision identifiers, used by Alembic.
revision = '0eee8c1abd3a'
down_revision = 'fcd9cebaa79c'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    op.add_column('projects', sa.Column('country', ARRAY(sa.String()), nullable=True))

    fetch_all_project_geoms = "SELECT id, ST_AsText(ST_GeomFromWKB(ST_AsEWKB(geometry))) from projects;"
    projects = conn.execute(fetch_all_project_geoms)

    for project in projects:
        project_id = project[0]
        project_polygon = shapely.wkt.loads(project[1])
        # country_match = []
        with open('migrations/countries.json') as countries_data:
            countries = json.load(countries_data)
            for country in countries['features']:
                country_polygon = shape(country['geometry'])
                is_match = country_polygon.contains(project_polygon)
                if is_match:
                    print(str(project_id) + ' in ' + country['properties']['ADMIN'])
                    # country_match.append(country['properties']['ADMIN'])
        # if len(country_match) > 0:
                update_country_info = "update projects " + \
                                      "set country = array_append(country, '{" + country['properties']['ADMIN'] + \
                                      "}') where id = " + str(project_id)

                op.execute(update_country_info)


def downgrade():
    op.drop_column('projects', 'country')
