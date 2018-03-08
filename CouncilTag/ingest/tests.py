from django.test import TestCase
from CouncilTag.ingest.tagging import TagEngine, RandomTagEngine
from CouncilTag.ingest.models import Committee, Agenda, AgendaItem, Tag
from CouncilTag.ingest.utils import time_check
from datetime import datetime
import calendar


class TestTaggingInterface(TestCase):
    
    def test_not_implementation(self):
        class TestTagEngine2(TagEngine):
            pass
        with self.assertRaises(Exception) as e:
            test = TestTagEngine2()
            self.assertEqual(e.msg, "test")
    

class TestRandomTagEngine(TestCase):

    def setUp(self):
        for i in range(0, 3):
            Tag(name="Tag" + str(i)).save()
        committee = Committee(name="Council")
        committee.save()
        agenda = Agenda(meeting_time=949494949, committee=committee)
        agenda.save()
        self.agenda_item = AgendaItem(title="test", department="test", agenda=agenda )
        self.agenda_item.save()
        self.tagengine = RandomTagEngine()

    def test_engine_applies_tags(self):
        self.assertEqual(0, len(self.agenda_item.tags.all()))
        tags_to_apply = self.tagengine.find_tags(self.agenda_item)
        self.assertEqual(2, len(tags_to_apply))
        self.assertNotEqual(tags_to_apply[0].name, tags_to_apply[1].name)
        self.tagengine.apply_tags(self.agenda_item, tags_to_apply)
        self.assertEqual(2, len(self.agenda_item.tags.all()))


class TestTimeCheckFunctionsCommand(TestCase):


    def setUp(self):
        committee = Committee(name="Council")
        committee.save()
        agenda = Agenda(meeting_time=1518571800, committee=committee)
        agenda.save()
        
    

    def test_time_check_function(self):
        now = datetime.now()
        val = time_check(now, 1518571800, 'before')
        self.assertEqual(True, val)

        val = time_check(now, 1518571800, 'after')
        self.assertEqual(False, val)

    
    def test_time_check_function_inputs(self):
        now = datetime.now()
        with self.assertRaises(Exception) as e:
            val = time_check(now, 1518571800, 'equals')
            self.assertEqual(e.exception.message, "Direction can only be 'before' or 'after'")
        
