import React, {ReactNode} from 'react';
import {Redirect, Route} from 'react-router-dom';
import { MainPage } from '../pages/Main/MainPage';
import { UserInfo } from '../pages/UserInfo/UserInfo';

interface AppRoute {
  title: string;
  url: string;
  page: React.FC;
  exact: boolean;
}

interface RouterProps {
  children?: ReactNode;
  setSelectedPage: (page: string) => void;
}

const routes: AppRoute[] = [
  {
    title: 'Main',
    url: '/home',
    page: MainPage,
    exact: true
  },
  {
    title: 'UserInfo',
    url: '/user-info',
    page: UserInfo,
    exact: true
  },
];

const Router: React.FC = () => (
  <div>
    { routes.map((route) => (
        <Route key={route.url} exact={route.exact} path={route.url} component={route.page}/>
    ))}
    <Route path="/" exact>
      <Redirect to="/user-info" />
    </Route>
  </div>
);

export default Router;
