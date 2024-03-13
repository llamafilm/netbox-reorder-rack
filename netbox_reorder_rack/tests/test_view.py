from dcim.models import Rack
from dcim.models import Site
from django.contrib.contenttypes.models import ContentType
from users.models import ObjectPermission
from utilities.testing import TestCase


class ReorderRackTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="Site 1", slug="site-1")
        Rack.objects.create(name="Rack 1", site=site, u_height=42)

    def test_reorder_rack_view_without_permissions(self):
        rack = Rack.objects.all().first()
        response = self.client.get(f"/dcim/racks/{rack.pk}/reorder/")
        self.assertHttpStatus(response, 403)

    def test_reorder_rack_view_with_permissions(self):
        # Add model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["change", "view"])
        obj_perm.save()
        obj_perm.users.add(self.user)
        ct = ContentType.objects.filter(model="device").first()
        obj_perm.object_types.add(ct)
        rack = Rack.objects.all().first()

        response = self.client.get(f"/dcim/racks/{rack.pk}/reorder/")
        self.assertHttpStatus(response, 200)
