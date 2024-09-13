from efootprint.abstract_modeling_classes.source_objects import SourceValue
from efootprint.core.hardware.servers.server_base_class import Server


class Autoscaling(Server):
    def __init__(self, name: str, carbon_footprint_fabrication: SourceValue, power: SourceValue,
                 lifespan: SourceValue, idle_power: SourceValue, ram: SourceValue, cpu_cores: SourceValue,
                 power_usage_effectiveness: SourceValue, average_carbon_intensity: SourceValue,
                 server_utilization_rate: SourceValue):
        super().__init__(
            name, carbon_footprint_fabrication, power, lifespan, idle_power, ram, cpu_cores, power_usage_effectiveness,
            average_carbon_intensity, server_utilization_rate)

    def update_nb_of_instances(self):
        hour_by_hour_nb_of_instances = self.raw_nb_of_instances.ceil()

        self.nb_of_instances = hour_by_hour_nb_of_instances.set_label(f"Hourly number of {self.name} instances")
