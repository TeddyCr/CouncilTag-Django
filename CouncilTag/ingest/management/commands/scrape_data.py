from django.core.management.base import BaseCommand, CommandError
from CouncilTag.ingest.models import Committee, Agenda, AgendaItem, AgendaRecommendation
from CouncilTag.ingest.data import get_data
from CouncilTag.ingest.utils import time_check
from datetime import datetime
from django.core.exceptions import *
from CouncilTag.ingest.tagging import RandomTagEngine
class Command(BaseCommand):
    help = 'Scrapes the Santa Monica website for meeting information'

    def save_agendaitem(self, agenda_item, new_agenda, meeting_time):
        random_tagger = RandomTagEngine()
        new_agenda_item = AgendaItem()
        for g in agenda_item:
            new_agenda_item.department = g['Department']
            new_agenda_item.title = g['Title']
            new_agenda_item.sponsors = g['Sponsors']
            new_agenda_item.meeting_time = meeting_time
            new_agenda_item.meeting_id = g['MeetingID']
            new_agenda_item.agenda_item_id = g['ID']
            if 'Body' in g:
              new_agenda_item.body = g['Body']
            else: 
              new_agenda_item.body = []
            new_agenda.save()
            new_agenda_item.agenda = new_agenda
            new_agenda_item.save()
            tags = random_tagger.find_tags(new_agenda_item)
            random_tagger.apply_tags(new_agenda_item, tags)
            if 'Recommendations' in g:
                  new_rec = AgendaRecommendation(recommendation=g['Recommendations'])
                  new_rec.agenda_item = new_agenda_item
                  new_rec.save()            

    def handle(self, *args, **options):
        try:
            committee = Committee.objects.get(name="Santa Monica City Council")
        except ObjectDoesNotExist:
            Committee(name="Santa Monica City Council", email="counciltag@gmail.com").save()
            committee = Committee.objects.get(name="Santa Monica City Council")
        years = [2016,2017,2018]
        agendas = dict()
        for year in years:
            agenda_values = get_data(year=year)
            for time, agenda in agenda_values.items():
              agendas[time] = agenda
        for meeting_time, agenda in agendas.items():
                      
            exists = Agenda.objects.filter(meeting_time = meeting_time).first()
            if (not exists):
              new_agenda = Agenda(meeting_time = meeting_time)
              new_agenda.committee = committee
              for ag in agenda:      
                  self.save_agendaitem(ag, new_agenda, meeting_time)
              new_agenda.save()