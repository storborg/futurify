import os.path
import os
import shutil

from unittest import TestCase

from .. import main


__here__ = os.path.dirname(__file__)
examples_dir = os.path.join(__here__, 'examples')
desired_dir = os.path.join(__here__, 'desired')
work_dir = os.path.join('/tmp', 'futurify-tests')


def files_match(a, b):
    with open(a) as fa:
        with open(b) as fb:
            return fa.read() == fb.read()


class TestFull(TestCase):

    def setUp(self):
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
            os.makedirs(work_dir)

    def copy_examples(self, dest):
        shutil.copytree(examples_dir, dest)

    def test_dry_run_unchanged(self):
        dest = os.path.join(work_dir, 'examples')
        self.copy_examples(dest)
        main(['futurify',
              '--silent',
              '--dry-run',
              '+absolute_import', '-print_function',
              dest])
        # Check that all files are unchanged.
        for fn in ('simple.py', 'multiline.py', 'complex.py', 'nonpython.txt'):
            self.assertTrue(files_match(os.path.join(examples_dir, fn),
                                        os.path.join(dest, fn)))

    def test_run(self):
        dest = os.path.join(work_dir, 'examples')
        self.copy_examples(dest)
        main(['futurify',
              '--silent',
              '+absolute_import', '-print_function',
              dest])
        # Check that files are changed correctly.
        for fn in ('simple.py', 'multiline.py', 'complex.py'):
            self.assertTrue(files_match(os.path.join(desired_dir, fn),
                                        os.path.join(dest, fn)))
        # Check that non *.py file was unchanged.
        fn = 'nonpython.txt'
        self.assertTrue(files_match(os.path.join(examples_dir, fn),
                                    os.path.join(dest, fn)))

    def test_nonexistent_path(self):
        path = os.path.join(work_dir, 'this-path-should-definitely-not-exist')
        with self.assertRaises(ValueError):
            main(['futurify',
                  '--silent',
                  '+print_function',
                  path])

    def test_usage_without_changes(self):
        with self.assertRaises(SystemExit):
            main(['futurify',
                  'hello'])

    def test_usage_without_paths(self):
        with self.assertRaises(SystemExit):
            main(['futurify',
                  '+print_function'])

    def test_call_with_file(self):
        dest = os.path.join(work_dir, 'examples')
        self.copy_examples(dest)
        main(['futurify',
              '--silent',
              '+absolute_import', '-print_function',
              os.path.join(dest, 'complex.py')])
        # Check that complex.py is changed correctly.
        fn = 'complex.py'
        self.assertTrue(files_match(os.path.join(desired_dir, fn),
                                    os.path.join(dest, fn)))
        # Check that other files are unchanged.
        for fn in ('simple.py', 'multiline.py', 'nonpython.txt'):
            self.assertTrue(files_match(os.path.join(examples_dir, fn),
                                        os.path.join(dest, fn)))
