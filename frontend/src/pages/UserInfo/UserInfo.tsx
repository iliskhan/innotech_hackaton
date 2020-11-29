import React from 'react';
import styles from './UserInfo.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';

import avatarPlaceholder from '../../assets/images/avatar_placeholder.jpg';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faVk} from '@fortawesome/free-brands-svg-icons'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import { useHistory } from 'react-router-dom';

type IProps = any;

const UserInfo = (props: IProps) => {
    const history = useHistory();
    const cx = classNames.bind(styles);
    const fetchedData = props.location.state?.referrer;
    console.log(fetchedData);

    // TODO: change this when backend will be ready
    const [avatar] = Object.values(fetchedData.files);

    return (
        <>
            <FontAwesomeIcon onClick={() => history.push('/')} className={cx(styles.backArrow)} icon={faArrowLeft} />
            <Grid
                container
                direction="column"
                justify="center"
                alignItems="center"
                className={cx(styles.container)}
            >
                <Grid
                    container
                    alignItems="center"
                    direction="column"
                    item xs={12} className={cx(styles.avatarContainer,)}
                >
                    <div className={cx(styles.avatarBackground)}>
                        <div className={cx(styles.avatar)}
                             style={{backgroundImage: `url(${avatar ? avatar : avatarPlaceholder})`,}}>
                        </div>
                    </div>
                    <h6><FontAwesomeIcon className={cx(styles.vkIcon)} icon={faVk}/> Открыть профиль</h6>
                    <h2 className={cx(styles.userName)}>Святослав Орлов</h2>
                </Grid>
                <Grid container direction="column" alignItems="center" item xs={12}
                      className={cx(styles.dataContainer,)}>
                    <Grid container justify="space-between" className={cx(styles.dataItem)}>
                        <span>Имя</span>
                        <span>Святослав</span>
                    </Grid>
                    <Grid container justify="space-between" className={cx(styles.dataItem)}>
                        <span>Фамилия</span>
                        <span>Орлов</span>
                    </Grid>
                    <Grid container justify="space-between" className={cx(styles.dataItem)}>
                        <span>Дата рождения</span>
                        <span>28/11/1985</span>
                    </Grid>
                    <Grid container justify="space-between" className={cx(styles.dataItem)}>
                        <span>Город</span>
                        <span>Москва</span>
                    </Grid>
                    <Grid container justify="space-between" className={cx(styles.dataItem)}>
                        <span>Место работы</span>
                        <span>Google</span>
                    </Grid>
                </Grid>
            </Grid>
        </>
    );
};

export {UserInfo};
