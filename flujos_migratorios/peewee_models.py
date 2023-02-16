from peewee import *

database = SqliteDatabase('sql.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Region(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'region'

class Demography(BaseModel):
    female_population_as_of_1_july_thousands = FloatField(null=True)
    individuals_using_the_internet_percent_of_population = FloatField(null=True)
    international_migrant_stock_percent_of_population = FloatField(null=True)
    international_migrant_stock_total = FloatField(null=True)
    male_population_as_of_1_july_thousands = FloatField(null=True)
    median_age_as_of_1_july_years = FloatField(null=True)
    multidimensional_poverty_headcount_ratio_percent_of_total_population = FloatField(null=True)
    net_migration_rate_per_1000_population = FloatField(null=True)
    net_number_of_migrants_thousands = FloatField(null=True)
    population_ages_014_percent_of_total_population = FloatField(null=True)
    population_density_people_per_sq_km_of_land_area = FloatField(null=True)
    population_growth_annual_percent = FloatField(null=True)
    population_in_largest_city = FloatField(null=True)
    population_in_the_largest_city_percent_of_urban_population = FloatField(null=True)
    refugee_population_by_country_or_territory_of_asylum = FloatField(null=True)
    refugee_population_by_country_or_territory_of_origin = FloatField(null=True)
    region = ForeignKeyField(column_name='region_id', field='id', model=Region)
    rural_population_growth_annual_percent = FloatField(null=True)
    rural_population_percent_of_total_population = FloatField(null=True)
    urban_population_growth_annual_percent = FloatField(null=True)
    urban_population_percent_of_total_population = FloatField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'demography'

class Economy(BaseModel):
    adjusted_net_national_income_current_us = FloatField(null=True)
    adjusted_net_national_income_per_capita_annual_percent_growth = FloatField(null=True)
    adjusted_savings_gross_savings_percent_of_gni = FloatField(null=True)
    cost_of_business_startup_procedures_female_percent_of_gni_per_capita = FloatField(null=True)
    cost_of_business_startup_procedures_male_percent_of_gni_per_capita = FloatField(null=True)
    cost_of_business_startup_procedures_percent_of_gni_per_capita = FloatField(null=True)
    domestic_credit_to_private_sector_by_banks_percent_of_gdp = FloatField(null=True)
    domestic_credit_to_private_sector_percent_of_gdp = FloatField(null=True)
    ease_of_doing_business_score_0__lowest_performance_to_100__best_performance = FloatField(null=True)
    foreign_direct_investment_net_bop_current_us = FloatField(null=True)
    gdp_current_us = FloatField(null=True)
    gdp_growth_annual_percent = FloatField(null=True)
    gini_index = FloatField(null=True)
    gni_current_us = FloatField(null=True)
    gni_growth_annual_percent = FloatField(null=True)
    gross_domestic_savings_current_us = FloatField(null=True)
    gross_domestic_savings_percent_of_gdp = FloatField(null=True)
    gross_savings_percent_of_gdp = FloatField(null=True)
    gross_savings_percent_of_gni = FloatField(null=True)
    industry_including_construction_value_added_annual_percent_growth = FloatField(null=True)
    industry_including_construction_value_added_percent_of_gdp = FloatField(null=True)
    inflation_consumer_prices_annual_percent = FloatField(null=True)
    investment_in_ict_with_private_participation_current_us = FloatField(null=True)
    labor_force_total = FloatField(null=True)
    labor_tax_and_contributions_percent_of_commercial_profits = FloatField(null=True)
    listed_domestic_companies_total = FloatField(null=True)
    market_capitalization_of_listed_domestic_companies_current_us = FloatField(null=True)
    market_capitalization_of_listed_domestic_companies_percent_of_gdp = FloatField(null=True)
    multidimensional_poverty_headcount_ratio_percent_of_total_population = FloatField(null=True)
    net_trade_in_goods_and_services_bop_current_us = FloatField(null=True)
    new_business_density_new_registrations_per_1000_people_ages_1564 = FloatField(null=True)
    new_businesses_registered_number = FloatField(null=True)
    personal_remittances_paid_current_us = FloatField(null=True)
    personal_remittances_received_current_us = FloatField(null=True)
    personal_remittances_received_percent_of_gdp = FloatField(null=True)
    profit_tax_percent_of_commercial_profits = FloatField(null=True)
    region = ForeignKeyField(column_name='region_id', field='id', model=Region)
    research_and_development_expenditure_percent_of_gdp = FloatField(null=True)
    researchers_in_rd_per_million_people = FloatField(null=True)
    tax_payments_number = FloatField(null=True)
    tax_revenue_percent_of_gdp = FloatField(null=True)
    taxes_on_income_profits_and_capital_gains_percent_of_total_taxes = FloatField(null=True)
    time_spent_dealing_with_the_requirements_of_government_regulations_percent_of_senior_management_time = FloatField(null=True)
    unemployment_total_percent_of_total_labor_force_modeled_ilo_estimate = FloatField(null=True)
    unemployment_total_percent_of_total_labor_force_national_estimate = FloatField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'economy'

class Education(BaseModel):
    educational_attainment_at_least_bachelors_or_equivalent_population_25_total_percent_cumulative = FloatField(null=True)
    educational_attainment_at_least_completed_lower_secondary_population_25_total_percent_cumulative = FloatField(null=True)
    educational_attainment_at_least_completed_upper_secondary_population_25_total_percent_cumulative = FloatField(null=True)
    educational_attainment_at_least_masters_or_equivalent_population_25_total_percent_cumulative = FloatField(null=True)
    educational_attainment_doctoral_or_equivalent_population_25_total_percent_cumulative = FloatField(null=True)
    region = ForeignKeyField(column_name='region_id', field='id', model=Region)
    technicians_in_rd_per_million_people = FloatField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'education'

class Employment(BaseModel):
    employers_total_percent_of_total_employment_modeled_ilo_estimate = FloatField(null=True)
    employment_in_agriculture_percent_of_total_employment_modeled_ilo_estimate = FloatField(null=True)
    employment_in_industry_percent_of_total_employment_modeled_ilo_estimate = FloatField(null=True)
    employment_in_services_percent_of_total_employment_modeled_ilo_estimate = FloatField(null=True)
    firms_offering_formal_training_percent_of_firms = FloatField(null=True)
    labor_force_total = FloatField(null=True)
    region = ForeignKeyField(column_name='region_id', field='id', model=Region)
    selfemployed_total_percent_of_total_employment_modeled_ilo_estimate = FloatField(null=True)
    time_required_to_register_property_days = FloatField(null=True)
    time_required_to_start_a_business_days = FloatField(null=True)
    time_required_to_start_a_business_female_days = FloatField(null=True)
    time_required_to_start_a_business_male_days = FloatField(null=True)
    unemployment_total_percent_of_total_labor_force_modeled_ilo_estimate = FloatField(null=True)
    unemployment_total_percent_of_total_labor_force_national_estimate = FloatField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'employment'

class Health(BaseModel):
    births_thousands = FloatField(null=True)
    cause_of_death_by_communicable_diseases_and_maternal_prenatal_and_nutrition_conditions_percent_of_total = FloatField(null=True)
    cause_of_death_by_noncommunicable_diseases_percent_of_total = FloatField(null=True)
    death_rate_crude_per_1000_people = FloatField(null=True)
    domestic_general_government_health_expenditure_per_capita_current_us = FloatField(null=True)
    domestic_private_health_expenditure_per_capita_current_us = FloatField(null=True)
    female_deaths_thousands = FloatField(null=True)
    female_life_expectancy_at_birth_years = FloatField(null=True)
    female_mortality_between_age_15_and_50_deaths_under_age_50_per_1000_females_alive_at_age_15 = FloatField(null=True)
    infant_deaths_under_age_1_thousands = FloatField(null=True)
    infant_mortality_rate_infant_deaths_per_1000_live_births = FloatField(null=True)
    intentional_homicides_per_100000_people = FloatField(null=True)
    male_deaths_thousands = FloatField(null=True)
    male_life_expectancy_at_birth_years = FloatField(null=True)
    male_mortality_between_age_15_and_50_deaths_under_age_50_per_1000_males_alive_at_age_15 = FloatField(null=True)
    mean_age_childbearing_years = FloatField(null=True)
    net_reproduction_rate_surviving_daughters_per_woman = FloatField(null=True)
    people_using_at_least_basic_drinking_water_services_percent_of_population = FloatField(null=True)
    people_with_basic_handwashing_facilities_including_soap_and_water_percent_of_population = FloatField(null=True)
    pregnant_women_receiving_prenatal_care_percent = FloatField(null=True)
    prevalence_of_moderate_or_severe_food_insecurity_in_the_population_percent = FloatField(null=True)
    region = ForeignKeyField(column_name='region_id', field='id', model=Region)
    suicide_mortality_rate_per_100000_population = FloatField(null=True)
    total_fertility_rate_live_births_per_woman = FloatField(null=True)
    underfive_deaths_under_age_5_thousands = FloatField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'health'

