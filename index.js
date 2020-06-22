import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Tax from '@/components/tax'
import TaxR from '@/components/taxr'
import TaxP from '@/components/taxp'
import Reports from '@/components/reports'
import Ref from '@/components/reference'
import TaxComp from '@/components/cit'
import Err from '@/components/NotFound'
import Proj from '@/components/projects'
import Profile from '@/components/profile'
import Messages from '@/components/profmessage'
import files from '@/components/SelectFiles'
import loged from '@/components/log'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/app',
      name: 'Home',
      component: Home
    },
    {
      path: '/logs',
      name: 'Log',
      component: loged
    },
    {
      path: '/test',
      name: 'test',
      component: files
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages
    },
    {
      path: '/income',
      name: 'computation',
      component: TaxComp
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/projs',
      name: 'Projects',
      component: Proj
    },
    {
      path: '/ref',
      name: 'Reference',
      component: Ref
    },
    {
      path: '/reports',
      name: 'Reports',
      component: Reports
    },
    {
      path: '/taxp',
      name: 'TP',
      component: TaxP
    },
    {
      path: '/taxr',
      name: 'TR',
      component: TaxR
    },
    {
      path: '/books',
      name: 'tax',
      component: Tax
    },
    {
      path: '*',
      name: 'err',
      component: Err
    }
  ],
  mode: 'history'
})
