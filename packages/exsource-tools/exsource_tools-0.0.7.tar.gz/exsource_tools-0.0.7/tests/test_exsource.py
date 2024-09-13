"""
Unit tests for tools.py
"""
import unittest
import os
import shutil
import yaml
from exsource_tools import load_exsource_file, ExSource
from exsource_tools.exsource import ExSourceExport
from exsource_tools import utils
from exsource_tools.exporters import OpenSCADExporter, CadQueryExporter, FreeCADExporter

TEST_PATH = os.path.dirname(__file__)

#pylint: disable=protected-access

# Docstrings have little value in the unit tests
#pylint: disable=missing-class-docstring
#pylint: disable=missing-function-docstring

class ExSourceTestCase(unittest.TestCase):

    def test_roundtrip(self):
        example_file = os.path.join(TEST_PATH, "examples", "readme_example.yml")
        with open(example_file, 'r', encoding="utf-8") as file_obj:
            input_data = yaml.safe_load(file_obj.read())
        exsource = load_exsource_file(example_file)
        self.assertEqual(exsource.dump(), input_data)

    def test_output_multiply_defined(self):
        example_file = os.path.join(TEST_PATH, "examples", "readme_example.yml")
        with open(example_file, 'r', encoding="utf-8") as file_obj:
            input_data = yaml.safe_load(file_obj.read())
        input_data["exports"]["another_frame"] = {"output-files": ["output/frame.step"],
                                                  "source-files": ["frame2.FCStd"],
                                                  "application": "freecad"}
        with self.assertLogs('exsource', level='WARN'):
            ExSource(input_data)

    def test_file_format(self):
        yaml_exts = ["exsource.yaml",
                     "exsource.yml",
                     "exsource-def.yaml",
                     "yaml.yml",
                     "json.yaml"]
        json_exts = ["exsource.json",
                     "exsource-def.json",
                     "yaml.json",
                     "json.json"]
        other_exts = ["exsource",
                      "exsource-def",
                      "exsource.xml",
                      "yaml",
                      "json"]
        for filename in yaml_exts:
            self.assertEqual(utils.exsource_file_format(filename), "YAML")
        for filename in json_exts:
            self.assertEqual(utils.exsource_file_format(filename), "JSON")
        for filename in other_exts:
            with self.assertRaises(ValueError) as context:
                utils.exsource_file_format(filename)
            self.assertTrue(f"Couldn't read '{filename}'." in str(context.exception))

class ExporterTestCase(unittest.TestCase):

    example_dir = os.path.join(TEST_PATH, "examples")

    def setUp(self):
        self.pwd = os.getcwd()
        os.chdir(self.example_dir)
        if os.path.exists('output'):
            shutil.rmtree('output')

    def tearDown(self):
        os.chdir(self.pwd)

    def _execution_script(self, application, exporterclass):
        example_file = "readme_example.yml"
        exsource = load_exsource_file(example_file)
        for _, export in exsource.exports.items():
            self.assertIsInstance(export, ExSourceExport)
            for output in export.output_files:
                self.assertFalse(os.path.exists(output.filepath), f"{output.filepath} exists")
            app = export.application
            if app.lower() == application:
                exporter = exporterclass(export, headless=True)
                exporter.process_export(output_file_statuses=dict())
                for output in export.output_files:
                    self.assertTrue(os.path.exists(output.filepath))

    def test_freecad(self):
        self._execution_script("freecad", FreeCADExporter)

    def test_openscad(self):
        self._execution_script("openscad", OpenSCADExporter)

    def test_cadquery(self):
        self._execution_script("cadquery", CadQueryExporter)
