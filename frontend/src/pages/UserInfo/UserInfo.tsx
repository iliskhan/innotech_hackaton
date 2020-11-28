import React from 'react';
import styles from './UserInfo.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';

const UserInfo = () => {
    const cx = classNames.bind(styles);

    return (
        <Grid className={cx(styles.container)} container>
            <Grid className={cx(styles.containerItem)} item sm={6}>
                UserInfo
            </Grid>
            <Grid className={cx(styles.containerItem)} item sm={6}>
               hello
            </Grid>
        </Grid>
    );
};

export { UserInfo };
