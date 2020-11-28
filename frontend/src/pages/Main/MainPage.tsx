import React from 'react';
import styles from './MainPage.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';

const MainPage = () => {
    const cx = classNames.bind(styles);

    return (
        <Grid className={cx(styles.container)} container>
            <Grid className={cx(styles.containerItem)} item sm={6}>
                MainPage
            </Grid>
            <Grid className={cx(styles.containerItem)} item sm={6}>
                home
            </Grid>
        </Grid>
    );
};

export { MainPage };
