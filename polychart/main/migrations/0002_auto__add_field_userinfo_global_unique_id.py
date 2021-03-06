# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

import hashlib, hmac, os, platform
from django.conf import settings
from base64 import urlsafe_b64encode

# Utility functions.
def random_code():
    # 18 random bytes -- more than a UUID, and looks nicer in base 64
    return urlsafe_b64encode(os.urandom(18))

server_hash = hashlib.sha256(str(settings.DEBUG) + platform.uname()[1]).hexdigest()
def get_unique_id(uid):
    return hmac.new(server_hash, str(uid), digestmod=hashlib.sha256).hexdigest()

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserInfo.global_unique_id'
        db.add_column(u'main_userinfo', 'global_unique_id',
                      self.gf('django.db.models.fields.CharField')(default=random_code, max_length=64),
                      keep_default=False)

        # Initializing values of global_unique_id to their previous values
        if not db.dry_run:
            for user in orm.UserInfo.objects.all():
                user.global_unique_id = get_unique_id(user.user_id)
                user.save()

        # Adding unique constraint on 'UserInfo', fields ['global_unique_id']
        db.create_unique(u'main_userinfo', ['global_unique_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'UserInfo', fields ['global_unique_id']
        db.delete_unique(u'main_userinfo', ['global_unique_id'])

        # Deleting field 'UserInfo.global_unique_id'
        db.delete_column(u'main_userinfo', 'global_unique_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'jca7ANxN4k4iv-ZDY74NGS6z'", 'unique': 'True', 'max_length': '128'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'spec_json': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.dashboarddatatable': {
            'Meta': {'object_name': 'DashboardDataTable'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Dashboard']"}),
            'data_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.DataSource']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'main.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'connection_type': ('django.db.models.fields.CharField', [], {'default': "'direct'", 'max_length': '16'}),
            'db_host_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'db_name_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'db_password_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'db_port_cipher': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'db_ssl_cert_cipher': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'db_unix_socket_cipher': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'db_username_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'ga_profile_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'89PizJX5c8pUpDjixEDNHeBy'", 'unique': 'True', 'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'oauth_refresh_token': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ssh_host_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'ssh_key_cipher': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ssh_port_cipher': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'ssh_username_cipher': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.event': {
            'Meta': {'object_name': 'Event'},
            'cid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'main.forgotpassword': {
            'Meta': {'object_name': 'ForgotPassword'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'AUpn0Wa251g8ZnnXwkVP1Qy7'", 'unique': 'True', 'max_length': '128'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.jsuserinfo': {
            'Meta': {'object_name': 'JSUserInfo'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '20'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        u'main.pendingdatasource': {
            'Meta': {'object_name': 'PendingDataSource'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'j_SwU1Mb2ZiWtQWEJGe8HPf7'", 'unique': 'True', 'max_length': '128'}),
            'params_json': ('django.db.models.fields.TextField', [], {})
        },
        u'main.tutorialcompletion': {
            'Meta': {'object_name': 'TutorialCompletion'},
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'global_unique_id': ('django.db.models.fields.CharField', [], {'default': "'qC4dLOin8gNdIaskUYSDK-co'", 'max_length': '64'}),
            'interest': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'secure_storage_salt': ('django.db.models.fields.CharField', [], {'default': "'Sv8H3uJAB7E='", 'max_length': '16'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'technical': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'usecase': ('django.db.models.fields.CharField', [], {'default': "'web'", 'max_length': '16'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['main']
