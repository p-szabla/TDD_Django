from django.urls import resolve
from django.test import TestCase
from list.views import home_page
from list.models import Item, List
from django.http import HttpRequest
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)



        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>Listy rzeczy do zrobienia</title>', response.content)
        # self.assertTrue(response.content.strip().endswith(b'</html>'))
    # def test_home_page_can_save_a_POST_request(self):
    #     request = HttpRequest()
    #     request.method = 'POST'
    #     request.POST['item_text'] = 'Nowy element listy'
    #
    #     response = home_page(request)
    #
    #     self.assertEqual(Item.objects.count(),1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text,'Nowy element listy')
    #
    #
    # def test_home_page_redirects_after_POST_request(self):
    #     request = HttpRequest()
    #     request.method = 'POST'
    #     request.POST['item_text'] = 'Nowy element listy'
    #
    #     response = home_page(request)
    #
    #     self.assertEqual(response.status_code,302)
    #     self.assertEqual(response['location'],'/lists/the-only-list-in-the-world')


    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(),0)

class ListAndItemModelTest(TestCase):

    def test_saving_and_retriving_items(self):
        list_ = List()
        list_.save()
        first_item=Item()
        first_item.text='Absolutnie pierwszy element listy'
        first_item.list=list_
        first_item.save()

        second_item=Item()
        second_item.text = 'Drugi element listy'
        second_item.list=list_
        second_item.save()

        saved_list = List.objects.first()

        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'Absolutnie pierwszy element listy')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.text,'Drugi element listy')
        self.assertEqual(second_saved_item.list,list_)




class ListViewTest(TestCase):

    def test_uses_list_templates(self):
        list_=List.objects.create()
        response = self.client.get(f'/list/{list_.id}/' )
        self.assertTemplateUsed(response,'list.html')

    def test_diplays_only_items_for_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='itemey a',list=other_list)
        Item.objects.create(text='itemey b',list=other_list)

        response = self.client.get(f'/list/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'itemey a')
        self.assertNotContains(response, 'itemey b')


    def uses_list_template(self):
        response = self.client.get('/lists/the-only-lists-in-the-world')
        self.assertTemplateUsed(response, 'list.html')



class NewListTest(TestCase):


    def test_home_saving_a_POST_request(self):

        self.client.post('/lists/new',data={'item_text':"Nowy element listy"})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'Nowy element listy')


    def test_home_page_redirects_after_POST_request(self):
        response = self.client.post('/lists/new',data={'item_text':"Nowy element listy"})

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/lists/the-only-list-in-the-world')
