import React from 'react';
import styles from './UserInfo.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';

import avatarPlaceholder from '../../assets/images/avatar_placeholder.jpg';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faVk} from '@fortawesome/free-brands-svg-icons'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import { useHistory } from 'react-router-dom';
import { Person } from '../../models/Person'

type IProps = any;

const UserInfo = (props: IProps) => {
    const history = useHistory();
    const cx = classNames.bind(styles);
    const fetchedData = props.location.state?.referrer;

    const person: any = new Person(fetchedData);
    const personDisplayData: [string, string | number][] = Object.entries(person);


    const {avatar, first_name, last_name, nickname, vk_user_id} = fetchedData;

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
                    <a href={`https://vk.com/id${vk_user_id}`} style={{
                        textDecoration: 'none',
                        color: 'black'
                    }} target="_blank">
                        <h6><FontAwesomeIcon className={cx(styles.vkIcon)} icon={faVk}/> Открыть профиль</h6>
                    </a>
                    <h2 className={cx(styles.userName)}>{first_name} {last_name} {nickname}</h2>
                </Grid>
                <Grid container direction="column" alignItems="center" item xs={12}
                      className={cx(styles.dataContainer,)}>
                    {personDisplayData.map(([name, value], index) => {
                        return <Grid key={index} container justify="space-between" className={cx(styles.dataItem)}>
                        <span>{name}</span>
                        <span>{value}</span>
                    </Grid>
                    })}
                    {/*<Grid container justify="space-between" className={cx(styles.dataItem)}>*/}
                    {/*    <span>Имя</span>*/}
                    {/*    <span>Святослав</span>*/}
                    {/*</Grid>*/}
                    {/*<Grid container justify="space-between" className={cx(styles.dataItem)}>*/}
                    {/*    <span>Фамилия</span>*/}
                    {/*    <span>Орлов</span>*/}
                    {/*</Grid>*/}
                    {/*<Grid container justify="space-between" className={cx(styles.dataItem)}>*/}
                    {/*    <span>Дата рождения</span>*/}
                    {/*    <span>28/11/1985</span>*/}
                    {/*</Grid>*/}
                    {/*<Grid container justify="space-between" className={cx(styles.dataItem)}>*/}
                    {/*    <span>Город</span>*/}
                    {/*    <span>Москва</span>*/}
                    {/*</Grid>*/}
                    {/*<Grid container justify="space-between" className={cx(styles.dataItem)}>*/}
                    {/*    <span>Место работы</span>*/}
                    {/*    <span>Google</span>*/}
                    {/*</Grid>*/}
                </Grid>
            </Grid>
        </>
    );
};

export {UserInfo};
